document.addEventListener('DOMContentLoaded', function() {
	if (document.querySelector('#follow_button') != null){
		const follow_button = document.querySelector('#follow_button');
		follow_button.addEventListener('click', async function() {
			const user_profile = document.querySelector('#user_profile').innerHTML;
			const login_user = document.querySelector('#login_user').innerHTML;
			const num_followers = document.querySelector('#followers');
			let new_followers = Number(num_followers.innerHTML);
			if (follow_button.innerHTML === 'Follow'){
				follow_button.innerHTML = 'Unfollow';
				new_followers = new_followers+1;
				num_followers.innerHTML = `${new_followers}`;
				await fetch(`../user/${login_user}`, {
					method: 'PUT',
					body: JSON.stringify({
						new_follower: user_profile
					})
				})
			}
			else {
				follow_button.innerHTML = 'Follow';
				new_followers = new_followers-1;
				num_followers.innerHTML = `${new_followers}`;
				await fetch(`../user/${login_user}`, {
					method: 'PUT',
					body: JSON.stringify({
						new_unfollower: user_profile
					})
				})
			}
		});
	}
});

async function like_function(post_id){
	const button = document.querySelector(`#like_button${post_id}`);
	const post_likes = document.querySelector(`#likes${post_id}`).innerHTML;
	if (button.innerHTML === 'Like'){
		button.innerHTML = 'Unlike';
		let new_likes = Number(post_likes) + 1;
		await fetch(`../posts/${post_id}`, {
			method: 'PUT',
			body: JSON.stringify({
				like: new_likes
			})
		});
		document.querySelector(`#likes${post_id}`).innerHTML = `${new_likes}`;
	}
	else {
		button.innerHTML = 'Like';
		let new_likes = Number(post_likes) - 1;
		await fetch(`../posts/${post_id}`, {
			method: 'PUT',
			body: JSON.stringify({
				like: new_likes
			})
		});
		document.querySelector(`#likes${post_id}`).innerHTML = `${new_likes}`;
	}

}

async function edit_text(post_id){
	const edit_button = document.querySelector(`#edit_button${post_id}`);
	const save_button = document.querySelector(`#save_button${post_id}`);
	const edit_area = document.querySelector(`#edit_area${post_id}`);
	const text = document.querySelector(`#content${post_id}`);
	if(edit_button.type === 'submit'){
		edit_button.type = 'hidden';
		save_button.type = 'submit';
		edit_area.style.display = 'block';
		text.style.display = 'none';
		edit_area.value = text.innerHTML;
	}
	else {
		edit_button.type = 'submit';
		save_button.type = 'hidden';
		edit_area.style.display = 'none';
		text.innerHTML = edit_area.value;
		text.style.display = 'block';

		await fetch(`../posts/${post_id}`, {
			method: 'PUT',
			body: JSON.stringify({
				new_text: text.innerHTML
			})
		});
	}
	return false;
}
