<template>
    <div  style="width:100%;height:650px;overflow:auto;"  :style="{height:theheight+'px'}">
		<iframe :src="src" style="width:100%;height:99%;"  frameborder=”no” border=”0″ marginwidth=”0″ marginheight=”0″ scrolling=”no” allowtransparency=”yes”></iframe>
    </div>
</template>
<script>
    export default {
        data () {
            return {
				theheight:'',
            }
        },
		mounted: function() {
			this.theheight=window.innerHeight-120;
		},
		computed: {
			// 仅读取，值只须为函数
			src: function () {
				return adapterUrl+'rightmanage/ui/index.html#/curruser';
			}
		}
    }
</script>
<style>
</style>