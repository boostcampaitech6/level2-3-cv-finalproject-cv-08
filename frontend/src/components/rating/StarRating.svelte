<script>

	import Star from './Star.svelte';
	
	// User rating states
	let rating = null;
	let hoverRating = null;
	
	// form interaction states
	let collectFeedback = false;
	let feedbackCompleted = false;
	
	let result ='';
	export let ABtype ;
	export let result_id;
	export let latest_id;
	
	// using curried function to initialize hover with id
	const handleHover = (id) => () => {
		hoverRating = id;
	} 
	const handleRate = (id) => (event) => {
		if (collectFeedback && 
				rating && 
				rating.toString() === event.srcElement.dataset.starid
		) {
			collectFeedback = false;
			return;
		}
		rating = id;
		collectFeedback = true;
		saveRating();
	} 
	
	let stars = [
		{ id: 1, title: 'One Star' },
		{ id: 2, title: 'Two Stars' },
		{ id: 3, title: 'Three Stars' },
		{ id: 4, title: 'Four Stars' },
		{ id: 5, title: 'Five Stars' },
	]

	
    function checkRating() {
        if (rating === null) {
            alert('별점을 선택해주세요.');
        } else {
			saveRating();
        }
    } 
    

	async function saveRating() {
    const token = sessionStorage.getItem('auth_token'); // sessionStorage에서 토큰 가져오기
	const formData = new FormData();
    formData.append('type',ABtype);
	formData.append('rating',rating);
	
    try {
        const response = await fetch(`https://api.makezenerator.com/api/v1/mz-request/${result_id}/mz-result/${latest_id}`, {
            method: 'PATCH',
            headers: {
                'Token': token,
      },
            body: formData,
        });

        if (response.ok) {
            const result = await response.json();
            alert(`별점 ${rating}점이 성공적으로 저장되었습니다.`);
        } else {
            const errorResponse = await response.json();
            console.error('Failed to save rating:', errorResponse);
        }
    } catch (error) {
        console.error('Error saving rating:', error);
    }
}

	
</script>
<style>
	.feedback {
		position: relative;
	}
	.collectFeedbackContainer {
		width: 300px;
		position: absolute;
		top: 44px;
		left: 0;
		background: #fff;
		border: 1px solid #666;
		padding: 8px;
		transition: transform .2s ease-out;
	}
	.collectFeedbackContainer textarea {
		display: block;
		width: 100%;
		height: 120px;
		resize: none;
	}
	.cancel {
		background: none;
		text-decoration: underline;
		border: none;
	}
	.starContainer {
		display: flex; 
        flex-direction: row; 
        gap: 4px;
		transition: background .2s ease-out;
		border-radius: 10px;
		padding: 4px 6px 0;
	}
	.feedbackContainer:hover .starContainer {
		background: #efefef;
	}
	.secondaryAction {
		margin: 8px;
		font-size: 12px;
		display: inline-block;
	}
	.feedbackContainerDisabled {
		pointer-events: none;
	}
	:global(button) {
		cursor: pointer;
	}
</style>

<div class="feedback"> 
	<span id="feedbackContiner" class="feedbackContainer" class:feedbackContainerDisabled={feedbackCompleted}>
		<span class="starContainer">
		{#each stars as star (star.id)}
			<Star 
					filled={hoverRating ? (hoverRating >= star.id) : (rating >= star.id)} 
					starId={star.id}
					on:mouseover={handleHover(star.id)} 
					on:mouseleave={() => hoverRating = null}
					on:click={handleRate(star.id)}
				/>
		{/each}
</div>