use std::{fs};

use pyo3::{exceptions::PyFileNotFoundError, prelude::*};

use crate::engine::{deck::Deck, session::{Session}};
mod engine;

#[pyclass]
pub struct Engine {
	#[pyo3(get)]
	test: String,

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
			test: "COUCOU".to_string(),
			deck,
			session })
	}
}

#[pyfunction]
fn status() -> String {
	"Rust Engine is running.".to_string()
}

#[pymodule]
fn anki_engine(m: &Bound<'_, PyModule>) -> PyResult<()> {
	m.add_function(wrap_pyfunction!(status, m)?)?;
	m.add_class::<Engine>()?;
	Ok(())
}