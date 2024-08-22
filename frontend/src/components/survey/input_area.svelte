<script>
    import { onMount } from 'svelte';

    export let value='';

    function autoGrow(oField) {
        if (oField.scrollHeight > oField.clientHeight) {
            oField.style.height = oField.scrollHeight + "px";
        }
    }

    onMount(() => {
        autoGrow(value); // 초기 로드 시 자동 높이 조정
    });
</script>

<style>
    .auto-grow-textarea {
        width: 100%; /* 전체 폭을 차지 */
        min-height: 50px; /* 최소 높이 */
        overflow-y: hidden; /* 스크롤바 숨기기 */
        padding: 8px; /* 패딩 조정 */
        box-sizing: border-box; /* 패딩을 포함한 총 너비 유지 */
        border: 1px solid #ccc; /* 테두리 스타일 */
        resize: none; /* 사용자가 크기 조절 못하게 함 */
        font-size: 15pt;
    }
</style>

<textarea bind:value class="auto-grow-textarea" on:input={e => autoGrow(e.target)}></textarea>
