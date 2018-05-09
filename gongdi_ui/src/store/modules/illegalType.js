import axios from 'axios';
const state = {
    datas:[],
	total:0,
	LSempdatas:[],
    IllegalTypelksdatas:[],
    isIllegalTypelkLoad:false,
	//isLoad:false,
	isLSempLoad:false,
	illegal_typetrees:[],
    isTreeload:false,
	isLSptypeLoad:false,
	userid:'',
	active:null,
	actionStatus:0, //0:nuknow,1:insert,2:edit,3:delete
	waitcomplete:false, //0:请求开始或已完成，1：请求中
}


// getters  在组件中要获得这个 state 里的 event, 那就需要写个getters
const getters = {
    illegal_types:state=>{
		return state.datas;
    },
    illegal_typetrees:state=>{
		return state.illegal_typetrees;
    },
	illegalTypesActionStatus:state=>{
		return state.actionStatus;
    },
	illegaltyplks:state=>{
        return state.IllegalTypelksdatas;
    },
	waitITstatus:state=>{
		return state.waitcomplete;
    },
}

// actions
const actions = {
    loadIllTyeTree ({ commit, state }) {
        if(!state.isTreeload){
			axios.get('/kong/gongdi_mng/v1.0/illegal__typetrees')
				.then(function(response){
					commit('loadIllTyeTree',response.data)
				}).catch(function(error){
				commit('loadIllTyeTree',response.data)
			})
        }
    },
    loadIllegalTypes ({ commit, state },data) {
		axios.get('/kong/gongdi_mng/v1.0/illegal_categorys/'+data+'/types',)
		.then(function(response){
			console.log("actions",response);
			commit('loadIllegalTypes',response.data)
		}).catch(function(error){
			//console.log("actions");
			commit('loadIllegalTypes',response.data)
		})
    },
	loadLeaveSystememp ({ commit, state }) {
		if (!state.isLSempLoad){
			axios.get('/kong/leave_system/v1.0/illegal_types')
			.then(function(response){
				commit('loadLeaveSystememp',response.data)
			}).catch(function(error){
				//console.log("actions");
				commit('loadLeaveSystememp',response.data)
			})
		}
    },
	loadIllegalTypelks ({ commit, state,dispatch }) {
        if(!state.isIllegalTypelkLoad){
            dispatch('getIllegalTypelks');
        }
    },
    getIllegalTypelks ({ commit}) {
		axios.get('/kong/gongdi_mng/v1.0/illegal_typelks')
			.then(function(response){
				console.log("actions",response);
				commit('loadIllegalTypelks',response.data)
			}).catch(function(error){
			//console.log("actions");
			commit('loadIllegalTypelks',response.data)
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
		axios.get('/kong/gongdi_mng/v1.0/illegal_types')
		.then(function(response){
			console.log("actions",response);
			commit('loademployee',response.data)
		}).catch(function(error){
			console.log(error);
			commit('loademployee',response.data)
		})
    },
	saveIllegal_type({ commit,state,dispatch},data){
		if (state.actionStatus==1){  // insert
			state.waitcomplete=true;
			axios.post('/kong/gongdi_mng/v1.0/illegal_types',data)
			.then(function(response){
				commit('insertedIllegal_type',{isSuccess:true,data:response.data});
                dispatch('getIllegalTypelks');
			}).catch(function(error){
				commit('insertedIllegal_type',{isSuccess:false})
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
				axios.put('/kong/gongdi_mng/v1.0/illegal_types/'+data['id'],modify)
				.then(function(response){
					commit('editedIllegal_type',{isSuccess:true,data:response.data});
                    dispatch('getIllegalTypelks');
				}).catch(function(error){
					commit('editedIllegal_type',{isSuccess:false})
				})  
			}else{
				state.actionStatus=0;
				state.active=null;
				state.waitcomplete=false;
			}
		}else if (state.actionStatus==3){  //delete
			axios.delete('/kong/gongdi_mng/v1.0/illegal_types/'+state.active['id'])
			.then(function(response){
				commit('deleteedIllegal_type',{isSuccess:true});
                dispatch('getIllegalTypelks');
			}).catch(function(error){
				commit('deleteedIllegal_type',{isSuccess:false})
			})
		}
	},
	editIllegal_type({ commit,state},{id}){
		commit('setIllegal_typeActive',{id:id});
		commit('editingIllegal_type');
	},
	removeIllegal_type({dispatch,commit,state},{id}){
		commit('setIllegal_typeActive',{id:id});
		commit('deleteingIllegal_type');
		dispatch('saveIllegal_type',{});
	},
}

// mutations 修改 state
const mutations = {
	setissuccess(state,data){
		state.issuccess=true;
		console.log(state.issuccess);
    },
    loadIllTyeTree(state,data){
        state.illegal_typetrees=data;
        state.isTreeload=true;
    },
    loadIllegalTypes(state,data){
		state.datas=data;
		//state.total=data.total
    },
    loadIllegalTypelks(state,data){
		state.isIllegalTypelkLoad=true;
		state.IllegalTypelksdatas=data;
    },
	resetemp(state){
        //state.employeedata=data;
		state.datas=[];
		//state.isLoad=false;
    },
	insertingIllegal_type(state,data){
		state.actionStatus=1;
    },
	insertedIllegal_type(state,{isSuccess,data}){
		state.waitcomplete=false;
		if (isSuccess){
			state.datas.push(data);
			state.active=null;
			state.actionStatus=0;
		}else{
			state.actionStatus=1;
		}
	},
	editingIllegal_type(state,data){
		state.actionStatus=2;//edit
    },
	editedIllegal_type(state,{isSuccess,data}){
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
	deleteingIllegal_type(state){
		state.actionStatus=3;
	},
	deleteedIllegal_type(state,{isSuccess}){
		if (isSuccess){
			state.datas=state.datas.filter(item =>item.id!=state.active['id']);
			state.actionStatus=0;
			state.active=null;
		}else{
			state.actionStatus=3;
		}
	},
	cancleIllegal_type(state){
		state.active=null;
		state.actionStatus=0;
	},
	setIllegal_typeActive(state,{id}){
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