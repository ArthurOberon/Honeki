use std::{fs, process};
// use std::sync::{Arc, Mutex}

mod engine;
use crate::engine::deck::Deck;
use crate::engine::session::Session;

// fn ctrl_c_handler(deck: &Deck) {


// 	ctrlc::set_handler(move ||{


// 	});
// }

fn main()
{
	let filename = "data/bones.json";

	let json = match fs::read_to_string(filename) {
		Ok(content) => content,
		Err(err) => {
			eprintln!("File error : {} does not exist : ({err}) .", filename);
			process::exit(1);
		}
	};

	let mut deck = match Deck::from_json(&json) {
		Ok(deck) => deck,
		Err(err) => {
			eprintln!("Syntax error in {} : ({err}) .", filename);
			process::exit(1);
		}
	};
	// println!("deck : {:#?}", deck);

	let mut session = Session::new(&mut deck);
	// println!("Session : {:#?}", session);

	session.launch(&mut deck);
}
