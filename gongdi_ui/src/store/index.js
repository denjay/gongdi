import Vue from 'vue'
import Vuex from 'vuex'
   
import mypermissions from './modules/mypermissions'
import illegalCategory from './modules/illegalCategory'
import illegalType from './modules/illegalType'
import subcontractors from './modules/subcontractors'
import empIllegal from './modules/empIllegal'
import subconIllegal from './modules/subconIllegal'
import danti from './modules/danti'
import gongdi from './modules/gongdi'
import buwei from './modules/buwei'
import inspect from './modules/inspect'
import guifan_tuzhi_tuji from './modules/guifan_tuzhi_tuji'
import jiaodi from './modules/jiaodi'
import doc_files from './modules/doc_files'
import doc from './modules/doc'

Vue.use(Vuex)


export default new Vuex.Store({
	state:{
		nowurl:'',
		screenheight:'',
	},
    modules: {
		illegalCategory,
		illegalType,
		subcontractors,
		mypermissions,
		empIllegal,
		subconIllegal,
		danti,
		gongdi,
		buwei,
		inspect,
		guifan_tuzhi_tuji,
		jiaodi,
		doc_files,
		doc
    }
})