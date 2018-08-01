// Get all the follow buttons from the dribbble follow page
a = document.querySelectorAll('.form-btn.light-btn.follow.compact');

// Convert the node list into an array
a = [...a]

a.forEach(button => {
	button.click()
})