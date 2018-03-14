<template>
    <div  style="width:100%;height:650px;">
		<iframe :src="src" style="width:100%;height:100%;"  frameborder=”no” border=”0″ marginwidth=”0″ marginheight=”0″ scrolling=”no” allowtransparency=”yes”></iframe>
    </div>
</template>
<script>
    export default {
        data () {
            return {
				
            }
        },
		computed: {
			// 仅读取，值只须为函数
			src: function () {
			   if(this.$route.params.aabb=='appuser')
					return adapterUrl+'rightmanage/ui/index.html#/appuser/hoursweb';
				else if(this.$route.params.aabb=='approle')
					return adapterUrl+'rightmanage/ui/index.html#/approle/hoursweb';
				else
					return adapterUrl+'rightmanage/ui/index.html#/curruser';
			}
		}
    }
</script>
<style>
</style>