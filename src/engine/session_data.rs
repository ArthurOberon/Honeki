#[derive(Debug, Clone)]
pub struct SessionData {
	pub new: usize,
	pub learning: usize,
	pub relearning: usize,
	pub review: usize,
}

impl SessionData {
	pub fn total(&self) -> usize {
		self.new + self.learning + self.relearning + self.review
	}
}
