import axios from 'axios';
const state = {
    data:{},
	superright:false,
    loaded:false,
	rightLoad:false

}

// getters  �������Ҫ������ state ��� event, �Ǿ���Ҫд��getters
const getters = {
    dailyformright:state=>state.data.dailyform||{},
	monthlyformright:state=>state.data.monthlyform||{},
	hourstatisticsright:state=>state.data.hourstatistics||{},
	lr_settingright:state=>state.data.lr_setting||{},
	abnormalstatisticsright:state=>state.data.abnormalstatistics||{},
	employeeright:state=>state.data.employee||{},
	leave_typeright:state=>state.data.leave_type||{},
	position_typeright:state=>state.data.position_type||{},
	departright:state=>state.data.depart||{},
	leave_applicationright:state=>state.data.leave_application||{},
	leave_checkright:state=>state.data.leave_check||{},
	annual_leave_balanceright:state=>state.data.annual_leave_balance||{},
	monthly_leaveright:state=>state.data.monthly_leaves||{},
	superright:state=>true,
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