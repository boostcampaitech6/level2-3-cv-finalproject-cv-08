<script>
    import { goto } from '$app/navigation';
    export let styleVariant = "outlined";
    let className = "";
    export { className as class };
    export let style;
    const variantsClassName = "style-variant-" + styleVariant;
    export let name = "Do something";
    export let type = "";
    

    async function reRequest() {

      const token = sessionStorage.getItem('auth_token');
      const result_id= sessionStorage.getItem('id');

      try {
        const response = await fetch(`https://api.makezenerator.com/api/v1/mz-request/${result_id}/mz-result`, {
          method: 'POST',
          headers: {
            'Token': token,
          },

          });
          if (response.ok) {
            alert('제출된 정보로 재생성 요청했습니다.');
            goto('/resultlist');
          }
          else{
            const errorResponse = await response.json();
            console.error('Failed to save rating:', errorResponse);
            alert(`재요철 실패: ${errorResponse.message}`);
          }
        
      } catch (error) {
        console.error('Error saving rating:', error);
        alert('재요청 중 에러가 발생했습니다.');

      }
    }
  </script>
  
  <button
  type = {type}
    on:click={reRequest}
    style="{'background: var(--neutral-10, #486284);border-radius: 50px; border-style: solid; border-color: var(--neutral-10, #486284); border-width: 1px; padding: 12px 20px 12px 20px; display: flex; flex-direction: row; gap: 10px; align-items: center; justify-content: center; position: relative; overflow: hidden;' + style}"
  >
    <div
      style="
        color: var(--neutral-0, #ffffff);
        text-align: left;
        font-family: var(--body-small-font-family, 'DmSans-Regular', sans-serif);
        font-size: var(--body-small-font-size, 22px);
        line-height: var(--body-small-line-height, 24px);
        font-weight: var(--body-small-font-weight, 400);
        position: relative;
      "
    >
      {name}
    </div>
  </button>