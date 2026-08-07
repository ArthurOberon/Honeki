use std::{fs::{self}};
use serde::{Serialize, Deserialize};
use chrono::Local;

use crate::engine::card::Card;


pub fn secure_save_file_from_json(path: &str, json: String) -> Result<(), Box<dyn std::error::Error>> {

	let tmp_file = format!("{path}.tmp");

	std::fs::write(&tmp_file, json)?;

	if let Err(err) = fs::rename(&tmp_file, path) {
		let _ = fs::remove_file(&tmp_file);
		return Err(Box::new(err));
	}	
	
	Ok(())
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Deck {
    pub cards: Vec<Card>,
	pub last_review_date: String,
	pub new_card_review_today: usize,
}

impl Deck {

	pub fn from_json(json: &str) -> Result<Self, serde_json::Error>
	{
		// let cards: Vec<Card> = serde_json::from_str(&json)?;
		// Ok(Deck { cards, last_review_date: "".to_string(), new_card_review_today: 0 })

		serde_json::from_str(json)
	}

	pub fn save_to_json(&self) -> Result<(), Box<dyn std::error::Error>>
	{
		let path = "data/bones.json";

		let json = serde_json::to_string_pretty(self)?;

		secure_save_file_from_json(path, json)?;

		Ok(())
	}

	pub fn reset_daily_stats(&mut self) {
		let today = Local::now().format("%Y-%m-%d").to_string();

		if self.last_review_date == "none" || self.last_review_date != today {
			self.last_review_date = today;
			self.new_card_review_today = 0;
		}
	}

	// pub fn len(&self) -> usize
	// {
	// 	self.cards.len()
	// }
}