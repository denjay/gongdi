import Vue from 'vue'
import Vuex from 'vuex'

import illegalCategory from './modules/illegalCategory'
import illegalType from './modules/illegalType' 
import mypermissions from './modules/mypermissions'
import danti from './modules/danti'
import gongdi from './modules/gongdi'
import buwei from './modules/buwei'
import inspect from './modules/inspect'
import guifan_tuzhi_tuji from './modules/guifan_tuzhi_tuji'
import jiaodi from './modules/jiaodi'

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
		gongdi,
		buwei,
		inspect,
		guifan_tuzhi_tuji,
		jiaodi
    }
})