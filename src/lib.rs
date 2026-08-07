#![allow(unsafe_op_in_unsafe_fn)]

use std::{fs};
use pyo3::{exceptions::PyFileNotFoundError, prelude::*};
use chrono::{NaiveDateTime};

use crate::engine::{
	deck::Deck,
	session::Session,
	session_data::SessionData,
	card::Card,
	// card::CardType,
	card::format_interval,
	card::Choice,
	card::get_next_good_interval
};

mod engine;

#[pyclass]
pub struct CardView {
	// Front
	#[pyo3(get)] name: String,

	// Back
	#[pyo3(get)] picture: String,
    #[pyo3(get)] placed_in: String,
    #[pyo3(get)] connect_to: Vec<String>,
    #[pyo3(get)] count: usize,

	// Metadata
	#[pyo3(get)] id: usize,
	// r_type: CardType,
	#[pyo3(get)] interval: f64,
	#[pyo3(get)] ease : f64,
    #[pyo3(get)] due: Option<NaiveDateTime>,
}

impl From<Card> for CardView {
	fn from(card: Card) -> Self {
		CardView {
			name: card.name,
			
			picture: card.picture,
			placed_in: card.placed_in,
			connect_to: card.connect_to,
			count: card.count,

			id: card.id,
			// r_type: card.r_type,
			interval: card.interval,
			ease: card.ease,
			due: card.due
		}
	}
}

#[pyclass]
pub struct SessionDataView {
	#[pyo3(get)] new: usize,
	#[pyo3(get)] learning: usize,
	#[pyo3(get)] relearning: usize,
	#[pyo3(get)] review: usize,
}

#[pymethods]
impl SessionDataView {
	#[getter]
	pub fn error(&self) -> usize {
		self.learning + self.relearning
	}
}

impl From<SessionData> for SessionDataView {
	fn from(data: SessionData) -> Self {
		SessionDataView {
			new: data.new,
			learning : data.learning,
			relearning : data.relearning,
			review : data.review,
		}
	}
}


#[pyclass]
pub struct Engine {
	deck: Deck,
	session: Session,
}

#[pymethods]
impl Engine {

	#[new]
	pub fn new() -> PyResult<Self> {
		let filename = "data/bones.json";

		let json = fs::read_to_string(filename).map_err(|err| {
			PyFileNotFoundError::new_err(format!("File error : {filename} does not exist : ({err})."))
		})?;
		
		let mut deck = Deck::from_json(&json).map_err(|err| {
			PyFileNotFoundError::new_err(format!("Syntax error in {filename} : ({err})."))
		})?;

		let session = Session::new(&mut deck);

		Ok(Engine {
			deck,
			session
		})
	}

	pub fn is_session_empty(&mut self) -> bool {
		self.session.is_empty()
	}

	pub fn get_data(&mut self) -> SessionDataView {
		let pure_data = self.session.data.clone();

		pure_data.into()
	}

	pub fn get_next_card(&mut self) -> Option<CardView> {
		if let Some(card_id) = self.session.next_card_id(&self.deck)
		{
			let pure_card = self.deck.cards[card_id].clone();
			
			Some(pure_card.into())
		}
		else {
			None
		}
	}

	pub fn get_string_formated_next_good_interval(&mut self, card: &CardView) -> String {
		format_interval(get_next_good_interval(card.interval, card.ease))
	}

	pub fn answer_card_review(&mut self, card_id: usize, answer: bool) {
		let choice = if answer {
			Choice::Right
		} else {
			Choice::Wrong
		};
		self.session.answer_card_review(&mut self.deck, card_id, choice);
	}

	pub fn clear_history(&mut self) {
		if let Err(err) = self.session.history.clear_and_save() {
			eprintln!("Error during history save process : {err}");
		}
	}

	pub fn undo(&mut self) -> bool {
		self.session.undo(&mut self.deck)
	}

	pub fn redo(&mut self) -> bool {
		self.session.redo(&mut self.deck)
	}

	pub fn get_config_json(&mut self) -> PyResult<String> {
		self.session.config.get_config_json()
	}

	pub fn save_config(&mut self, json_str: String) -> PyResult<()> {
		self.session.update_config(json_str, &self.deck)?;

		if let Err(err) = self.session.config.save_to_json() {
			eprintln!("Error during history save process: {err}");
		}

		Ok(())
	}

}

#[pymodule]
fn anki_engine(m: &Bound<'_, PyModule>) -> PyResult<()> {
	m.add_class::<Engine>()?;
	Ok(())
}