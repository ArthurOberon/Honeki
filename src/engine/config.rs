use core::fmt;
use std::fs::{read_to_string};
use serde::{Serialize, Serializer, Deserialize, Deserializer};
use chrono::{Duration};

mod duration_as_minutes {
	use super::*;

	pub fn deserialize<'de, D>(deserializer: D) -> Result<Duration, D::Error>
	where
		D: Deserializer<'de>,
	{
		let minutes = i64::deserialize(deserializer)?;
		Ok(Duration::minutes(minutes))
	}
	
	pub fn serialize<S>(duration: &Duration, serializer: S) -> Result<S::Ok, S::Error>
	where
		S: Serializer,
	{
		serializer.serialize_i64(duration.num_minutes())
	} 

}

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct SessionConfig {
	pub number_new_by_day: usize,

    #[serde(rename = "LAT", with = "duration_as_minutes")]
	pub lat : Duration, // Learn Ahead Time

	pub new_random_review : bool, // Does the new cards are shown in a random order
	pub new_random_select : bool, // Does the new cards are select in a random order
}

impl fmt::Debug for SessionConfig {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> fmt::Result {
		f.debug_struct("SessionConfig")
			.field("number_new_by_day", &self.number_new_by_day)
			.field("LAT", &format_args!("{} min", &self.lat.num_minutes()))
			.field("new_random_review", &self.new_random_review)
			.field("new_random_select", &self.new_random_select)
			.finish()
	}
}

impl Default for SessionConfig {
	fn default() -> Self {
		Self {
			number_new_by_day: 20,
			lat: Duration::minutes(20),
			new_random_review: false,
			new_random_select: false
		}
	}
}

impl SessionConfig {

	pub fn load_or_default() -> Self {
		let json = match read_to_string("config/config.json") {
			Ok(content) => content,
			Err(_) => {
				println!("Caution : File 'config/config.json' does not exist. Use the default configuration.");
				return Self::default();
			}
		};

		serde_json::from_str(&json).unwrap_or_else(|err| {
			eprintln!("Caution : File 'config/config.json' as syntax error : ({err}). Use the default configuration.");
			return Self::default();
		})
	}
}