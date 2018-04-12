export default [
	{
		path: '/',
		component: resolve => require(['./components/common/main.vue'], resolve),
		children:[
		{
			path: '/:path/:subPath/:page',
			component: resolve => require(['./components/common/container.vue'], resolve)
		},{

			path:'/rightmanage/:aabb',
			component:resolve => require(['./components/common/rightmanage.vue'], resolve)
		  
		}		
			
		]
	}
]
