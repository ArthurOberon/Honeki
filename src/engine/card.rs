use serde::{Serialize, Deserialize};
use chrono::{Duration, Local, NaiveDateTime};

use crate::engine::review::Choice;

pub const ONE_MINUTE: f64 = 1.0 / 1440.0;
pub const TEN_MINUTES: f64 = 10.0 / 1440.0;
pub const ONE_DAY: f64 = 1.0;

fn format_round_num(num: f64) -> String {
	let rounded = (num * 10.0).round() / 10.0;

	if rounded.fract() == 0.0 {
		format!("{:.0}", rounded)
	} else {
		format!("{:.1}", rounded)
	}
}

pub fn format_interval(days: f64) -> String {
	let minutes = days * 1440.0;

	if minutes < 60.0 {
		format!("{:.0}m", minutes)
	} else if days < 30.0 {
		format!("{:.0}d", days)
	} else {
		format!("{}mo", format_round_num(days / 30.0))
	}
}

pub fn format_interval_verbose(days: f64) -> String {
	let minutes = days * 1440.0;

	if minutes < 60.0 {
		format!("{:.0} min", minutes)
	} else if days < 30.0 {
		if days.round() <= 1.0 {
			"1 day".to_string()
		} else {
			format!("{:.0} days", days)
		}
	} else {
		let month_formatted = format_round_num(days / 30.0);	
		if month_formatted == "1" {
			"1 month".to_string()
		} else {
			format!("{} months", month_formatted)
		}
	}
}

#[derive(Serialize, Deserialize, Debug, Clone, Copy, PartialEq)]
pub enum CardType {
	Manual,
	Learn,
	Relearn,
	Review,
}

// #[serde(rename_all = "FORMAT")] -> to say to serde that the json will be write in FORMAT format - and he need to convert for write into this structure
// #[serde(rename = "NAME")] -> for ask serde to do only this with the var (to put on top of the var)

#[derive(Serialize, Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
pub struct Card {
	// Front
	pub name: String,

	// Back
	pub picture: String,
    pub placed_in: String,
    pub connect_to: Vec<String>,

	// Metadata
	pub id: usize,
	#[serde(rename = "type")]
	pub r_type: CardType,
	pub interval: f64,
	pub ease : f64,
    pub due: Option<NaiveDateTime>,
}

impl Card {
	// =====================================
	// === Section : Update Card
	// =====================================

	pub fn update_metadata(&mut self, choice : Choice)
	{
		match (self.r_type, choice) {
			(CardType::Manual, _) => {
				self.interval = ONE_MINUTE;
				self.ease = 2.5;
				self.r_type = CardType::Learn;
			}

			(CardType::Learn | CardType::Relearn, Choice::Wrong) => {
				self.interval = ONE_MINUTE;
			},
			(CardType::Learn | CardType::Relearn, Choice::Right) => {
				if self.interval == ONE_MINUTE {
					self.interval = TEN_MINUTES;
				}
				else if self.interval == TEN_MINUTES {
					self.interval = ONE_DAY;
					self.r_type = CardType::Review;
				}
			}

			(CardType::Review, Choice::Wrong) => {
				self.interval = TEN_MINUTES;
				self.r_type = CardType::Relearn;
				if self.ease > 0.13 {
					self.ease -= 0.2;
				}
			}
			(CardType::Review, Choice::Right) => {
				self.interval = (self.interval * self.ease).round();
			}
		}

		// set the due of the card into the new one (new = now + interval)
		self.update_due();

	}

	fn calculate_new_due(&self) -> NaiveDateTime
	{
		let now = Local::now().naive_local();
	
		let seconds = (self.interval * 86400.0).round() as i64;
		let duration = Duration::seconds(seconds);
	
		now + duration
	}

	pub fn update_due(&mut self)
	{
		self.due = Some(self.calculate_new_due());
		println!("\nCard put in {:?}. Next time seeing it : {}", self.r_type, format_interval_verbose(self.interval));
	}

}

	// -------------------------------------------
impl Card {
	// =====================================
	// === Section : Getter & Queries
	// =====================================

	// pub fn is_type(&self, r_type: CardType) -> bool
	// {
	// 	self.r_type == r_type
	// }

	// pub fn is_due(&self, time: NaiveDateTime) -> bool
	// {
	// 	self.due <= Some(time)
	// }

	pub fn is_due_now(&self) -> bool
	{
		let now = chrono::Utc::now().naive_utc();	
		match self.due {
			Some(due) => due <= now,
			None => false,
		}
	}

	pub fn is_due_today(&self) -> bool
	{
		let today = chrono::Utc::now().naive_utc().date();	
		
		match self.due {
			Some(due) => due.date() <= today,
			None => false,
		}
	}

	pub fn is_due_lat(&self, lat: Duration) -> bool
	{
		let now = chrono::Utc::now().naive_utc();
		match self.due {
			Some(due) => now - due <= lat,
			None => false
		}
	}

}
