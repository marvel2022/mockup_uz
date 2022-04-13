function core_method_js($this){
	var slug = $this.dataset.slug
	
	console.log('slug:', slug)


	if (user == 'AnonymousUser'){
		console.log("User is not logged in")
	}else{
		console.log("User is logged in")
		// updateUserOrder(pk, action, pageid)
    }
    download_counter(slug)	
}


function download_counter(slug){
	console.log('User is authenticated, sending data...')

	var url = '/ajax/download_counter/'

	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'Accept': 'application/json',
			'X-CSRFToken':csrftoken,
		}, 
		body:JSON.stringify({'slug':slug})
	})
	.then((response) => {
	   return response.json();
	})
	.then((data) => {
		console.log(data['success'])
	});
}


function like_unlike($this){
	var slug = $this.dataset.slug
	
	console.log('slug:', slug)


	if (user == 'AnonymousUser'){
		console.log("User is not logged in")
		alert('You are not allowed for this action, please login/sign-up')
	}else{
		console.log("User is logged in")
		like_unlike_method(slug)
    }
    // download_counter(slug)	
}


function like_unlike_method(slug){
	console.log('User is authenticated, sending data...')

	var url = '/ajax/like/mockup/'

	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'Accept': 'application/json',
			'X-CSRFToken':csrftoken,
		}, 
		body:JSON.stringify({'slug':slug})
	})
	.then((response) => {
	   return response.json();
	})
	.then((data) => {
		console.log(data['success'])
		window.location.reload(); 
	});
}