use std::fs::read_to_string;
use chrono::NaiveDateTime;
use serde::{Serialize, Deserialize};

use crate::engine::{
	card::{Card, CardType},
	deck::secure_save_file_from_json,
};

#[derive(Serialize, Deserialize, Debug)]
pub struct CardSnapshot {
    pub card_id: usize,

    pub prev_interval: f64,
    pub prev_ease: f64,
    pub prev_type: CardType,
    pub prev_due: Option<NaiveDateTime>,

    // pub prev_session_queue: CardType, -> know by prev_type (same thing)
    // pub prev_session_queue_pos: usize, -> always remove the first element
    // pub is_prev_new_card: bool, -> know by prev_type
}

impl CardSnapshot {
	pub fn card_to_snapshot(card: &Card) -> Self {

		Self {
			card_id: (card.id),
			prev_interval: (card.interval),
			prev_ease: (card.ease),
			prev_type: (card.r_type),
			prev_due: (card.due)
		}
	}
}


#[derive(Serialize, Deserialize, Debug)]
pub struct History {
    undo_stack: Vec<CardSnapshot>,
    redo_stack: Vec<CardSnapshot>,
}

impl Default for History {
    fn default() -> Self {
        Self {
            undo_stack: Vec::new(),
            redo_stack: Vec::new(),
        }
    }
}

impl History {
	pub fn load_or_default() -> Self {
		let path = "data/history.json";
		
		let json = match read_to_string(path) {
			Ok(content) => content,
			Err(_) => {
				let default_history = Self::default();
				if let Err(err) = default_history.save_to_json() {
					eprintln!("Error: Can't create the file {path}: {err}.");
				}

				return default_history;
			}	
		};
		
		serde_json::from_str(&json).unwrap_or_else(|err| {
			eprintln!("Caution : File 'data/history.json' as syntax error : ({err}). Can't use it.");

			let default_history = Self::default();
			if let Err(err) = default_history.save_to_json() {
				eprintln!("Error: Can't create the file {path}: {err}.");
			}

			default_history
		})
	}

	pub fn save_to_json(&self) -> Result<(), Box<dyn std::error::Error>> {
		let path = "data/history.json";

		let json = serde_json::to_string_pretty(self)?;
		secure_save_file_from_json(path, json)?;

		Ok(())
	}

	pub fn clear_and_save(&mut self) -> Result<(), Box<dyn std::error::Error>> {
		self.undo_stack.clear();
		self.redo_stack.clear();
		self.save_to_json()
	}
	
}

impl History {
	pub fn record_action(&mut self, snap: CardSnapshot) {
		self.undo_stack.push(snap);

		self.redo_stack.clear();
	}

	pub fn pop_undo(&mut self) -> Option<CardSnapshot> {
		self.undo_stack.pop()
	}

	pub fn push_undo(&mut self, snap: CardSnapshot) {
		self.undo_stack.push(snap);
	}

	pub fn pop_redo(&mut self) -> Option<CardSnapshot> {
		self.redo_stack.pop()
	}

	pub fn push_redo(&mut self, snap: CardSnapshot) {
		self.redo_stack.push(snap);
	}



}