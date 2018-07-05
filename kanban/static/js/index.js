dragula([
	document.getElementById('todo'),
	document.getElementById('doing'),
	document.getElementById('done'),
])

	.on('drag', function (el) {

		// add 'is-moving' class to element being dragged
		el.classList.add('is-moving');
	})
	.on('dragend', function (el) {

		// remove 'is-moving' class from element after dragging has stopped
		el.classList.remove('is-moving');

		var parentRef = el.parentElement.id;
		console.log(parentRef)
		console.log(el.id);

		var url = "/_update_kind/";
		fetch(url, {
			method: 'POST',
			body: JSON.stringify({ 
				"new_kind" : parentRef,
				"issue_id" : parseInt(el.id),
			}),
			headers: {
				'Content-Type': 'application/json'
			}
		}).then(res => res.json())
			.catch(error => console.error('Error:', error))
			.then(response => console.log(response));

		// add the 'is-moved' class for 600ms then remove it
		window.setTimeout(function () {
			el.classList.add('is-moved');
			window.setTimeout(function () {
				el.classList.remove('is-moved');
			}, 600);
		}, 100);
	});

