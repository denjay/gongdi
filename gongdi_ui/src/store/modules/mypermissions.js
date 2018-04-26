import axios from 'axios';
const state = {
    data:{},
	superright:true,
    loaded:false,
	rightLoad:false
}

// getters  �������Ҫ������ state ��� event, �Ǿ���Ҫд��getters
const getters = {
	employeeright:state=>state.data.employee||{},
	illegal_category_right:state=>state.data.illegal_category||{},
	illegal_type_right:state=>state.data.illegal_type||{},
	subcontractors_right:state=>state.data.subcontractors||{},
	emp_illegal_right:state=>state.data.emp_illegal||{},
	subcon_illegal_right:state=>state.data.subcon_illegal||{},
	danti_right:state=>state.data.danti||{},
	gongdi_right:state=>state.data.gongdi||{},
	buwei_right:state=>state.data.buwei||{},
	inspect_right:state=>state.data.inspect||{},
	guifan_right:state=>state.data.guifan||{},
	tuzhi_right:state=>state.data.tuzhi||{},
	tuji_right:state=>state.data.tuji||{},
	jiaodi_right:state=>state.data.inspect||{},
	super_right:state=>state.superright,
}

// actions
const actions = {
    loadpermissions ({ commit, state }) {
		if (!state.loaded){			
			axios.get(adapterUrl+'rightmanage/v1.0/cur-permissions?systemname=hoursweb')
			.then(function(response){
				commit('loadpermissions',response.data)
			}).catch(function(error){
				commit('loadpermissions','')
			})
		}
    }
}

// mutations �޸� state
const mutations = {
    loadpermissions(state,data){
        state.data=data;
        state.loaded=true;
    },
	loadsuperright(state,data){
        state.superright=data.data;
		state.rightLoad=true;
    },
	resetsuperright(state){
        state.superright=false;
		state.rightLoad=false;
    },
}

export default {
    state,
    getters,
    actions,
    mutations
}