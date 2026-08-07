use chrono::{NaiveDateTime};
use rand::seq::{SliceRandom};
use pyo3::{PyResult};

use crate::engine::{
	deck::Deck,
	card::CardType,
	card::Choice,
	session_data::SessionData,
	config::SessionConfig,
	history::CardSnapshot,
	history::History,
};

#[derive(Debug)]
pub struct Session {
	pub config: SessionConfig,

	pub new: Vec<usize>,
	pub learning: Vec<usize>,
	pub relearning: Vec<usize>,
	pub review: Vec<usize>,

	pub data: SessionData,
    pub rev_new_ratio: usize,
    pub rev_new_count: usize,

	pub history: History,
}

impl Session {

	// =====================================
	// === Section : Initialization
	// =====================================

	pub fn new(deck: &mut Deck) -> Self
	{
		deck.reset_daily_stats();

		let config = SessionConfig::load_or_default();
		let history = History::load_or_default();

		let mut learning = Vec::new();
		let mut relearning = Vec::new();
		let mut review = Vec::new();

		for card in deck.cards.iter() {
			if card.is_due_today() {
				match card.r_type {
					CardType::Manual => {},
					CardType::Learn => learning.push(card.id),
					CardType::Relearn => relearning.push(card.id),
					CardType::Review => review.push(card.id),
				}
			}
		}

        // sort in order of due (result : like interval but also with due as subsort) (nearest first)
        review.sort_by(|&a, &b| {
            deck.cards[a].due.cmp(&deck.cards[b].due)
        });

		let mut session = Session {
			config,
			new: Vec::new(),
			learning,
			relearning,
			review,
			data: SessionData::default(),
			rev_new_ratio: 0,
			rev_new_count: 0,
			history
		};

		session.apply_config_to_queues(deck);

		session
	}


	pub fn update_data(&mut self) {
		self.data = SessionData{
			new: self.new.len(),
			learning: self.learning.len(),
			relearning: self.relearning.len(),
			review: self.review.len()
		};
	}

	pub fn update_config(&mut self, json_str: String, deck: &Deck) -> PyResult<()> {
		self.config.update_config(json_str)?;

		self.apply_config_to_queues(deck);

		Ok(())
	}

	fn apply_config_to_queues(&mut self, deck: &Deck) {
		let mut rng = rand::thread_rng();

		let mut all_new: Vec<usize> = deck.cards.iter()
			.filter(|c| c.r_type == CardType::Manual).map(|c| c.id).collect();

		if self.config.new_random_select {
			all_new.shuffle(&mut rng);
		}

		let new_for_today = self.config.number_new_by_day.saturating_sub(deck.new_card_review_today);

		self.new = all_new.into_iter().take(new_for_today).collect();

		if self.config.new_random_review {
			self.new.shuffle(&mut rng);
		}
		
		self.rev_new_ratio = if !self.new.is_empty() {
			self.review.len() / self.new.len()
		} else {
			0
		};
		
		self.update_data();
	}

	pub fn is_empty(&mut self) -> bool {
		!(self.new.is_empty() && self.learning.is_empty() && self.relearning.is_empty() && self.review.is_empty())
	}

}



impl Session {
	// =====================================
	// === Section : Undo & Redo
	// =====================================

	fn remove_card_from_queue(&mut self, card_id: usize, prev_queue: CardType) //, due : Option<NaiveDateTime>)
	{
		// small local help function
		let remove_card_from = |vec: &mut Vec<usize>| {
			if let Some(pos) = vec.iter().position(|&id| id == card_id) {
				vec.remove(pos);
			}
		};
		
		match prev_queue {
			CardType::Manual => remove_card_from(&mut self.new),
			CardType::Learn => remove_card_from(&mut self.learning),
			CardType::Relearn => remove_card_from(&mut self.relearning),
			CardType::Review => remove_card_from(&mut self.review),
		}	
	}

	pub fn undo(&mut self, deck: &mut Deck) -> bool {

		let snapshot = match self.history.pop_undo() {
			Some(s) => s,
			None => return false,
		};

		let card = &mut deck.cards[snapshot.card_id];

		self.history.push_redo(CardSnapshot::card_to_snapshot(card));

		self.remove_card_from_queue(snapshot.card_id, card.r_type);

		// undo card metadatas
		card.interval = snapshot.prev_interval;
		card.ease = snapshot.prev_ease;
		card.r_type = snapshot.prev_type;
		card.due = snapshot.prev_due;

		// put card into his previous queue
		match snapshot.prev_type {
			CardType::Manual => {
				self.new.insert(0, snapshot.card_id);
				self.rev_new_count = self.rev_new_count.saturating_sub(1);
				deck.new_card_review_today = deck.new_card_review_today.saturating_sub(1);
			},
			CardType::Learn => self.learning.insert(0, snapshot.card_id),
			CardType::Relearn => self.relearning.insert(0, snapshot.card_id),
			CardType::Review => self.review.insert(0, snapshot.card_id),
		}

		self.update_data();

		// println!("Save process...");
		if let Err(err) = deck.save_to_json() {
			eprintln!("Error during deck save process : {err}");
		}

		// println!("Save process...");
		if let Err(err) = self.history.save_to_json() {
			eprintln!("Error during history save process : {err}");
		}

		true
	}
	
	pub fn redo(&mut self, deck: &mut Deck) -> bool {

		let snapshot = match self.history.pop_redo() {
			Some(s) => s,
			None => return false,
		};

		let card = &mut deck.cards[snapshot.card_id];

		self.history.push_undo(CardSnapshot::card_to_snapshot(card));

		self.remove_card_from_queue(snapshot.card_id, card.r_type);

		// undo card metadatas
		card.interval = snapshot.prev_interval;
		card.ease = snapshot.prev_ease;
		card.r_type = snapshot.prev_type;
		card.due = snapshot.prev_due;

		// put card into his previous queue
		match snapshot.prev_type {
			CardType::Manual => {
				self.new.insert(0, snapshot.card_id);
				self.rev_new_count += 1;
				if self.rev_new_count >= self.rev_new_ratio {
					self.rev_new_count = 0;
				}
				if deck.new_card_review_today < self.config.number_new_by_day {
					deck.new_card_review_today += 1;
				}
			},
			CardType::Learn => self.learning.insert(0, snapshot.card_id),
			CardType::Relearn => self.relearning.insert(0, snapshot.card_id),
			CardType::Review => {
				if card.is_due_today() {
					self.review.insert(0, snapshot.card_id)
				}
			},
		}

		self.update_data();

		// println!("Save process...");
		if let Err(err) = deck.save_to_json() {
			eprintln!("Error during deck save process : {err}");
		}

		// println!("Save process...");
		if let Err(err) = self.history.save_to_json() {
			eprintln!("Error during history save process : {err}");
		}

		true
	}
}


impl Session {
	// =====================================
	// === Section : Next Card Algorithm
	// =====================================

	fn pop_earliest_learning_or_relearning(&mut self, deck: &Deck) -> Option<usize>
	{
		match (self.learning.first(), self.relearning.first()) {
			// Which card from error (learn + relearn) have the sooner due ?
			(Some(&learn_index), Some(&relearn_index)) => {
				if deck.cards[learn_index].due < deck.cards[relearn_index].due {
					self.learning.first().copied()
				} else {
					self.relearning.first().copied()
				}
			}
			
			(Some(_), None) => self.learning.first().copied(),
			(None, Some(_)) => self.relearning.first().copied(),

			(None, None) => None
		}
	}

	pub fn next_card_id(&mut self, deck: &Deck) -> Option<usize>
	{
		// Get the index of the first element only if the due is now (now or past)
		let learn_index = self.learning.first().is_some_and(|&idx| deck.cards[idx].is_due_now());
		let relearn_index = self.relearning.first().is_some_and(|&idx| deck.cards[idx].is_due_now());

		// Priorize soon error card
		if learn_index || relearn_index {
			self.pop_earliest_learning_or_relearning(deck)
		}
		else
		{
			// Select a new card if the ratio say so
			if !self.new.is_empty()
			{
				self.rev_new_count += 1;
				if self.rev_new_count >= self.rev_new_ratio {
					self.rev_new_count = 0;
					return self.new.first().copied();
				}
			}

			// Look for card into review
			if !self.review.is_empty()
			{
				// Priorize Learning Ahead Time card (card due now or soon)
				if deck.cards[self.review[0]].is_due_lat(self.config.lat) {
					self.review.first().copied()
				}
				// Choose a random card in review
				else {
					// let rand_index = (0..self.review.len()).choose(&mut rand::thread_rng())?;
					// Some(self.review.remove(rand_index))
					self.review.choose(&mut rand::thread_rng()).copied()
				}
			}
			// Get a new card
			else if !self.new.is_empty() {
				self.new.first().copied()
			}
			// Get a error card (learn + relearning) not past due
			// OR no card anymore
			else {
				self.pop_earliest_learning_or_relearning(deck)
			}
		}
	}
}

impl Session {
	// =====================================
	// === Section : Launch Session
	// =====================================

	fn requeue_card(&mut self, deck: &mut Deck, card_id: usize, r_type: CardType, due : NaiveDateTime)
	{
		let target_vec = match r_type {
			CardType::Learn => Some(&mut self.learning),
			CardType::Relearn => Some(&mut self.relearning),
			_ => None,
		};

		if let Some(vec) = target_vec {	
			let pos = vec.binary_search_by(|&index| { 
				deck.cards[index].due.cmp(&Some(due))
			}).unwrap_or_else(|pos| pos);

			vec.insert(pos, card_id);
		}
	}

	pub fn answer_card_review(&mut self, deck: &mut Deck, card_id: usize, choice: Choice) {

		{
			let card = &mut deck.cards[card_id];
			
			let before_update_queue = card.r_type;

			self.history.record_action(CardSnapshot::card_to_snapshot(card));
	
			// from user input, update the card's metadatas (interval, r_type, ease, due) 
			card.update_metadata(choice);
			
			self.remove_card_from_queue(card_id, before_update_queue);
			
			if before_update_queue == CardType::Manual && deck.new_card_review_today < self.config.number_new_by_day {
				deck.new_card_review_today += 1;
			}
			
		}

		// println!("Save process...");
		if let Err(err) = deck.save_to_json() {
			eprintln!("Error during deck save process : {err}");
		}

		// println!("Save process...");
		if let Err(err) = self.history.save_to_json() {
			eprintln!("Error during history save process : {err}");
		}

		let r_type = deck.cards[card_id].r_type;
		let due = deck.cards[card_id].due.unwrap();

		if matches!(r_type, CardType::Learn | CardType::Relearn) {
			self.requeue_card(deck, card_id, r_type, due);
		}

		self.update_data();

	}

	// pub fn launch(&mut self, deck: &mut Deck) //-> bool
	// {
	// 	// to clear shell screen and reset the cursor
	// 	print!("\x1B[2J\x1B[H"); // \x1B: ESC, [2J: clear screen, [H: move cursor to top-left
	// 	io::stdout().flush().unwrap(); // Flush stdout buffer to execute this sequence immediately
	
	// 	println!("Session.Config : {:#?}", self.config);
	// 	// println!("Session.new: {:#?}", self.new);
	// 	// println!("Session.learning: {:#?}", self.learning);
	// 	// println!("Session.relearning: {:#?}", self.relearning);
	// 	// println!("Session.review: {:#?}", self.review);
	// 	println!("Session.Data : {:#?}", self.data);
	// 	// println!("Session.History : {:#?}", self.history);
		
	// 	println!("Enter [Enter] to start your session of today.");
	// 	wait_enter_input();


	// 	let len = self.data.total();

	// 	if len == 0
	// 	{
	// 		println!("No card to review today. Or You're already reviewed all the card for today.");
	// 		return;
	// 	}

	// 	while let Some(card_id) = self.next_card_id(deck) {
	// 		// to clear shell screen and reset the cursor
	// 		print!("\x1B[2J\x1B[H"); // \x1B: ESC, [2J: clear screen, [H: move cursor to top-left
	// 		io::stdout().flush().unwrap(); // Flush stdout buffer to execute this sequence immediately

	// 		println!("--- Card {} ---", card_id + 1);
	// 		println!("--- {} - {} - {} ---", self.data.new, self.data.learning + self.data.relearning, self.data.review);

	// 		let current_card = &mut deck.cards[card_id];

	// 		let before_review_queue = current_card.r_type;

	// 		if let Some(action) = review_one_card(current_card, &mut self.history) {
	// 			match action {
	// 				UserAction::Undo => {
	// 					if !self.undo(deck) {
	// 						println!("Nothing to undo.");
	// 						wait_enter_input();
	// 					}
	// 				},
	// 				UserAction::Redo => {
	// 					if !self.redo(deck) {
	// 						println!("Nothing to redo.");
	// 						wait_enter_input();
	// 					}
	// 				},
	// 				UserAction::Quit => {
	// 					println!("Quit the session.");
	// 					break;
	// 				},
	// 				UserAction::Answer(_) => unreachable!(),
	// 			}
	// 		} else {

	// 			self.remove_card_from_queue(card_id, before_review_queue);

	// 			if before_review_queue == CardType::Manual && deck.new_card_review_today < self.config.number_new_by_day {
	// 				deck.new_card_review_today += 1;
	// 			}

	// 			// println!("Save process...");
	// 			if let Err(err) = deck.save_to_json() {
	// 				eprintln!("Error during deck save process : {err}");
	// 			}

	// 			// println!("Save process...");
	// 			if let Err(err) = self.history.save_to_json() {
	// 				eprintln!("Error during history save process : {err}");
	// 			}

	// 			let r_type = deck.cards[card_id].r_type;
	// 			let due = deck.cards[card_id].due.unwrap();

	// 			if matches!(r_type, CardType::Learn | CardType::Relearn) {
	// 				self.requeue_card(deck, card_id, r_type, due);
	// 			}

	// 			self.update_data();

	// 			// println!("Session : {:#?}", self);

	// 			wait_enter_input();
	// 		}

	// 	}

	// 	// println!("Session : {:#?}", self);
	// 	if self.data.total() == 0 {
	// 		println!("Session end.");
	// 		println!("Congratulation for finishing your session day !");
	// 		if let Err(err) = self.history.clear_and_save() {
	// 				eprintln!("Error during history save process : {err}");
	// 			}
	// 	}
    // }
	
}