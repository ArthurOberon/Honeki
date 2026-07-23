use pyo3::prelude::*;


// NEXT TO DO :
// 	Create class to give to python with :
// 	-	element (Deck, Session, etc.)
// 	-	function (get_card, get_session, submit_answer, etc.)


#[pyfunction]
fn status() -> String {
	"Rust Engine is running.".to_string()
}

#[pymodule]
fn anki_engine(m: &Bound<'_, PyModule>) -> PyResult<()> {
	m.add_function(wrap_pyfunction!(status, m)?)?;
	Ok(())
}