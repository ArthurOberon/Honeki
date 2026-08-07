use core::fmt;
use std::fs::{read_to_string};
use pyo3::{PyResult, exceptions::PyValueError};
use serde::{Serialize, Serializer, Deserialize, Deserializer};
use chrono::{Duration};

use crate::engine::deck::secure_save_file_from_json;

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
			lat: Duration::minutes(10),
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

	pub fn get_config_json(&mut self) -> PyResult<String> {
		match serde_json::to_string(self) {
			Ok(json_str) => Ok(json_str),
			Err(err) => {
				Err(PyValueError::new_err(format!("Error of json serialize: ({err})")))
			}
		}
	}

	pub fn update_config(&mut self, json_str: String) -> PyResult<()> {
		let config: SessionConfig = match serde_json::from_str(&json_str) {
			Ok(c) => c,
			Err(err) => {
				return Err(PyValueError::new_err(format!("Error of parsing: ({err})")))
			}
		};

		println!("new config config: {:#?}", config);

		*self = config;

		println!("new config self: {:#?}", self);

		Ok(())
	}

	pub fn save_to_json(&self) -> Result<(), Box<dyn std::error::Error>> {
		let path = "config/config.json";

		let json = serde_json::to_string_pretty(self)?;
		secure_save_file_from_json(path, json)?;

		Ok(())
	}
}