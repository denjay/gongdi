import Vue from 'vue'
import Vuex from 'vuex'

import illegalCategory from './modules/illegalCategory'
import illegalType from './modules/illegalType' 
import mypermissions from './modules/mypermissions'
import danti from './modules/danti'
import gongdi from './modules/gongdi'

Vue.use(Vuex)


export default new Vuex.Store({
	state:{
		nowurl:'',
		screenheight:'',
	},
    modules: {
		illegalCategory,
		illegalType,
		mypermissions,
		danti,
		gongdi
    }
})