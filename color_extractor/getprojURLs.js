// Get all cards on homepage
cards = document.querySelectorAll('.dribbble-link')

// Spread node list into an array
cards = [...cards]

// Iterate over each and get the url
var urls = []
cards.forEach(card => {
	urls.push(card.href)
})