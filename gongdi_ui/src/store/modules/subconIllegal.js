import axios from 'axios';
const state = {
    datas:[],
	total:0,
	LSempdatas:[],
    illegal_pics:[],
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
    subcon_illegals:state=>{
		return state.datas;
    },
    sillegal_pics:state=>{
        return state.illegal_pics;
    },
    subcon_illegalstotal:state=>{
        return state.total;
    },
	LSsubcon_illegals:state=>{
		return state.LSempdatas;
    },
	subconIllegalStatus:state=>{
		return state.actionStatus;
    },
	waitSIstatus:state=>{
		return state.waitcomplete;
    },
	MLempdatas:state=>{
		return state.MLempdatas;
    },
}

// actions
const actions = {
    loadSubconIllegals ({ commit, state },data) {
		axios.get('/kong/gongdi_mng/v1.0/subcon_illegals',{params: data})
		.then(function(response){
			console.log("actions",response);
			commit('loadSubconIllegals',response)
		}).catch(function(error){
			//console.log("actions");
			commit('loadSubconIllegals',error)
		})
    },
	loadLeaveSystememp ({ commit, state }) {
		if (!state.isLSempLoad){
			axios.get('/kong/leave_system/v1.0/subcon_illegals')
			.then(function(response){
				commit('loadLeaveSystememp',response.data)
			}).catch(function(error){
				//console.log("actions");
				commit('loadLeaveSystememp',response.data)
			})
		}
    },
	loadLpemployee ({ commit, state },data) {
		axios.get('/kong/gongdi_mng/v1.0/subcon_illegals_lk',{params: data})
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
		axios.get('/kong/gongdi_mng/v1.0/subcon_illegals')
		.then(function(response){
			console.log("actions",response);
			commit('loademployee',response.data)
		}).catch(function(error){
			console.log(error);
			commit('loademployee',response.data)
		})
    },
	saveSubconIllegal({ commit,state},data){	
		if (state.actionStatus==1){  // insert
			state.waitcomplete=true;
			axios.post('/kong/gongdi_mng/v1.0/subcon_illegals',data)
			.then(function(response){
				commit('insertedSubconIllegal',{isSuccess:true,data:response.data});
			}).catch(function(error){
				commit('insertedSubconIllegal',{isSuccess:false})
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
				axios.put('/kong/gongdi_mng/v1.0/subcon_illegals/'+data['id'],modify)
				.then(function(response){
					commit('editedSubconIllegal',{isSuccess:true,data:response.data});
				}).catch(function(error){
					commit('editedSubconIllegal',{isSuccess:false})
				})  
			}else{
				state.actionStatus=0;
				state.active=null;
				state.waitcomplete=false;
			}
		}else if (state.actionStatus==3){  //delete
			axios.delete('/kong/gongdi_mng/v1.0/subcon_illegals/'+state.active['id'])
			.then(function(response){
				commit('deleteedSubconIllegal',{isSuccess:true});
			}).catch(function(error){
				commit('deleteedSubconIllegal',{isSuccess:false})
			})
		}
	},
	editSubconIllegal({ commit,state},{id}){
		commit('setSubconIllegalActive',{id:id});
		commit('editingSubconIllegal');
	},
	removeSubconIllegal({dispatch,commit,state},{id}){
		commit('setSubconIllegalActive',{id:id});
		commit('deleteingSubconIllegal');
		dispatch('saveSubconIllegal',{});
	},
	getSIllegal_pics({dispatch,commit,state},{id}){
        axios.get('/kong/gongdi_mng/v1.0/illegal/'+id+'/pics')
            .then(function(response){
                commit('getSIllegal_pics',response.data)
            }).catch(function(error){
            commit('getSIllegal_pics',response.data)
        })
    },
    removeSPic({dispatch,commit,state},{id}){
        axios.delete('/kong/gongdi_mng/v1.0/illegal_pics/'+id)
            .then(function(response){
                if(response.status === 204){
                    commit('removeSPic',id)
                }
            }).catch(function(error){

        })
    }
}

// mutations 修改 state
const mutations = {
	setissuccess(state,data){
		state.issuccess=true;
		console.log(state.issuccess);
    },
    loadSubconIllegals(state,data){
		state.datas=data.data;
		state.total=parseInt(data.headers['x-total']);
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
	insertingSubconIllegal(state,data){
		state.actionStatus=1;
    },
	insertedSubconIllegal(state,{isSuccess,data}){
		state.waitcomplete=false;
		if (isSuccess){
			state.datas.push(data);
            state.total+=1;
			state.active=null;
			state.actionStatus=0;
		}else{
			state.actionStatus=1;
		}
	},
	editingSubconIllegal(state,data){
		state.actionStatus=2;//edit
    },
	editedSubconIllegal(state,{isSuccess,data}){
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
	deleteingSubconIllegal(state){
		state.actionStatus=3;
	},
	deleteedSubconIllegal(state,{isSuccess}){
		if (isSuccess){
			state.datas=state.datas.filter(item =>item.id!=state.active['id']);
            state.total-=1;
			state.actionStatus=0;
			state.active=null;
		}else{
			state.actionStatus=3;
		}
	},
	cancleSubconIllegal(state){
		state.active=null;
		state.actionStatus=0;
	},
	setSubconIllegalActive(state,{id}){
		state.active=state.datas.find(item =>item.id==id);
		//console.log(id);
	},
    getSIllegal_pics(state,data){
        state.illegal_pics=data;
    },
    clearSIllegal_pics(state,data){
        state.illegal_pics=[];
    },
    removeSPic(state,id){
        console.log(id)
        state.illegal_pics=state.illegal_pics.filter(item =>item.id!=id);
    },
}

export default {
    state,
    getters,
    actions,
    mutations
}