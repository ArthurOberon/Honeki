use std::io::{self};

use crate::engine::card::{Card, ONE_DAY, ONE_MINUTE, TEN_MINUTES};
use crate::engine::card::format_interval;
use crate::engine::history::CardSnapshot;
use crate::engine::history::History;

pub enum Choice {
	Wrong,
	Right,
}

pub enum UserAction {
	Answer(Choice),
	Undo,
	Redo,
	Quit,
}

pub fn wait_enter_input()
{
	let mut input = String::new();
	io::stdin().read_line(&mut input).expect("Failed to read line");
}

fn print_front_card(name: &String)
{
	println!("Enter [Enter] to flip the card.");

    println!("\t{}", name);
}

fn print_back_card(card: &Card)
{
    println!("{:#?}\n", card);
    // println!("\tpicture:{:?}", card.picture);
    // println!("\tplaced_in:{:?}", card.placed_in);
    // println!("\tconnect_to:{:?}", card.connect_to);
}

fn get_user_choice(interval: f64, ease: f64) -> UserAction
{
	let next_good_interval = match interval {
		0.0 => ONE_MINUTE,
		ONE_MINUTE => TEN_MINUTES,
		TEN_MINUTES => ONE_DAY,
		_ =>  (interval * ease).round()
	};

    println!("Did you remember :");
    println!("[1] : No (1m) | [2] : Yes ({}) | [Z] : Undo | [Y] : Redo | [Q] : Quit",
		format_interval(next_good_interval));

    loop {

        let mut input = String::new();       
        io::stdin().read_line(&mut input).expect("Failed to read line");

		match input.trim().to_lowercase().as_str() {
			"1" => break UserAction::Answer(Choice::Wrong),
			"2" => break UserAction::Answer(Choice::Right),
			"z" => break UserAction::Undo,
			"y" => break UserAction::Redo,
			"q" => break UserAction::Quit,
			_ => println!("Not available choice ! Enter [1] or [2]"),
		}
    }
}

pub fn review_one_card(card : &mut Card, history: &mut History) -> Option<UserAction>
{
	print_front_card(&card.name);
	wait_enter_input();
	print_back_card(card);


	// get the user input (or direcly return false if the input is quit)
	let choice = match get_user_choice(card.interval, card.ease) {
		UserAction::Answer(c) => c,
		action => return Some(action),
	};

	history.record_action(CardSnapshot::card_to_snapshot(card));

	// from user input, update the card's metadatas (interval, r_type, ease, due) 
	card.update_metadata(choice);

	None
}
