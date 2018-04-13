import axios from 'axios';
const state = {
    datas:[],
	total:0,
	LSempdatas:[],
	//isLoad:false,
	isLSempLoad:false,
	isLSptypeLoad:false,
	userid:'',
	active:null,
	actionStatus:0, //0:nuknow,1:insert,2:edit,3:delete
	waitcomplete:false, //0:请求开始或已完成，1：请求中
}


// getters  在组件中要获得这个 state 里的 event, 那就需要写个getters
const getters = {
    emp_illegals:state=>{
		return state.datas;
    },
	emp_illegalstotal:state=>{
		return state.total;
    },
	LSemp_illegals:state=>{
		return state.LSempdatas;
    },
	empIllegalActionStatus:state=>{
		return state.actionStatus;
    },
	waitETstatus:state=>{
		return state.waitcomplete;
    },
}

// actions
const actions = {
    loadEmpIllegals ({ commit, state },data) {
		axios.get('/kong/gongdi_mng/v1.0/emp_illegals',{params: data})
		.then(function(response){
			console.log("actions",response);
			commit('loadEmpIllegals',response.data)
		}).catch(function(error){
			//console.log("actions");
			commit('loadEmpIllegals',response.data)
		})
    },
	loadLeaveSystememp ({ commit, state }) {
		if (!state.isLSempLoad){
			axios.get('/kong/leave_system/v1.0/emp_illegals')
			.then(function(response){
				commit('loadLeaveSystememp',response.data)
			}).catch(function(error){
				//console.log("actions");
				commit('loadLeaveSystememp',response.data)
			})
		}
    },
	loadLpemployee ({ commit, state },data) {
		axios.get('/kong/gongdi_mng/v1.0/emp_illegals_lk',{params: data})
		.then(function(response){
			console.log("actions",response);
			commit('loademployee',response.data)
		}).catch(function(error){
			//console.log("actions");
			commit('loademployee',response.data)
		})
    },
	loadMlemployee ({ commit, state },data) {   
		axios.get('/kong/leave_system/v1.0/company/'+data+'/employee',)
		.then(function(response){
			console.log("actions",response);
			commit('loadMlemployee',response.data)
		}).catch(function(error){
			//console.log("actions");
			commit('loadMlemployee',response.data)
		})
    },
	loadDepartFE({ commit, state },data) {
		axios.get('/kong/gongdi_mng/v1.0/department',{params: data})
		.then(function(response){
			commit('loadDepartFE',response.data)
		}).catch(function(error){
			//console.log("actions");
			commit('loadDepartFE',response.data)
		})
    },
	loadPosition_typeFE({ commit, state },data) {
		if (!state.isLSptypeLoad){
			axios.get('/kong/gongdi_mng/v1.0/position_types')
			.then(function(response){
				commit('loadPosition_typeFE',response.data)
			}).catch(function(error){
				//console.log("actions");
				commit('loadPosition_typeFE',response.data)
			})
		}
    },
	getemployee ({ commit, state }) {
		axios.get('/kong/gongdi_mng/v1.0/emp_illegals')
		.then(function(response){
			console.log("actions",response);
			commit('loademployee',response.data)
		}).catch(function(error){
			console.log(error);
			commit('loademployee',response.data)
		})
    },
	saveEmpIllegal({ commit,state},data){	
		if (state.actionStatus==1){  // insert
			state.waitcomplete=true;
			axios.post('/kong/gongdi_mng/v1.0/emp_illegals',data)
			.then(function(response){
				commit('insertedEmpIllegal',{isSuccess:true,data:response.data});
			}).catch(function(error){
				commit('insertedEmpIllegal',{isSuccess:false})
			})
		}else if (state.actionStatus==2){  // edit
			state.waitcomplete=true;
			var modify={},hasProp=false;
			console.log(state.active);
			for (var key in data){
				if ((key!='id')&&(state.active[key]!=data[key])){
					modify[key]=data[key];
					hasProp=true;
				}
			};
			//console.log(modify);
			if (hasProp){
				axios.put('/kong/gongdi_mng/v1.0/emp_illegals/'+data['id'],modify)
				.then(function(response){
					commit('editedEmpIllegal',{isSuccess:true,data:response.data});
				}).catch(function(error){
					commit('editedEmpIllegal',{isSuccess:false})
				})  
			}else{
				state.actionStatus=0;
				state.active=null;
				state.waitcomplete=false;
			}
		}else if (state.actionStatus==3){  //delete
			axios.delete('/kong/gongdi_mng/v1.0/emp_illegals/'+state.active['id'])
			.then(function(response){
				commit('deleteedEmpIllegal',{isSuccess:true});
			}).catch(function(error){
				commit('deleteedEmpIllegal',{isSuccess:false})
			})
		}
	},
	editEmpIllegal({ commit,state},{id}){
		commit('setEmpIllegalActive',{id:id});
		commit('editingEmpIllegal');
	},
	removeEmpIllegal({dispatch,commit,state},{id}){
		commit('setEmpIllegalActive',{id:id});
		commit('deleteingEmpIllegal');
		dispatch('saveEmpIllegal',{});
	},
}

// mutations 修改 state
const mutations = {
	setissuccess(state,data){
		state.issuccess=true;
		console.log(state.issuccess);
    },
    loadEmpIllegals(state,data){
		state.datas=data;
		//state.total=data.total
    },
	loadLeaveSystememp(state,data){
		state.isLSempLoad=true;
		state.LSempdatas=data;		
    },
	resetemp(state){
        //state.employeedata=data;
		state.datas=[];
		//state.isLoad=false;
    },
	insertingEmpIllegal(state,data){
		state.actionStatus=1;
    },
	insertedEmpIllegal(state,{isSuccess,data}){
		state.waitcomplete=false;
		if (isSuccess){
			state.datas.push(data);
			state.active=null;
			state.actionStatus=0;
		}else{
			state.actionStatus=1;
		}
	},
	editingEmpIllegal(state,data){
		state.actionStatus=2;//edit
    },
	editedEmpIllegal(state,{isSuccess,data}){
		state.waitcomplete=false;	
		if (isSuccess){
			//state.datas.push(data);
			for (var key in data){
				state.active[key]=data[key];
			};
			state.actionStatus=0;
			state.active=null;
		}else{
			state.actionStatus=2;
		}
	},
	deleteingEmpIllegal(state){
		state.actionStatus=3;
	},
	deleteedEmpIllegal(state,{isSuccess}){
		if (isSuccess){
			state.datas=state.datas.filter(item =>item.id!=state.active['id']);
			state.actionStatus=0;
			state.active=null;
		}else{
			state.actionStatus=3;
		}
	},
	cancleEmpIllegal(state){
		state.active=null;
		state.actionStatus=0;
	},
	setEmpIllegalActive(state,{id}){
		state.active=state.datas.find(item =>item.id==id);
		//console.log(id);
	},
	setuserid(state,userid){
		state.userid=userid;
	}
}

export default {
    state,
    getters,
    actions,
    mutations
}