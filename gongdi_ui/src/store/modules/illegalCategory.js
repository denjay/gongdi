import axios from 'axios';
const state = {
    datas:[],
	total:0,
	LSempdatas:[],
	departFEdatas:[],//部门资料
	MLempdatas:[],//请假系统月报表所需要的员工数据
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
    illegal_categorys:state=>{
		return state.datas;
    },
	illegal_categorystotal:state=>{
		return state.total;
    },
	LSillegal_categorys:state=>{
		return state.LSempdatas;
    },
	illegalCategoryActionStatus:state=>{
		return state.actionStatus;
    },
	waitICStatus:state=>{
		return state.waitcomplete;
    },
	departFEdatas:state=>{
		return state.departFEdatas;
    },
	MLempdatas:state=>{
		return state.MLempdatas;
    },
}

// actions
const actions = {
    loadIllegalCategorys ({ commit, state }) {
		axios.get('/kong/gongdi_mng/v1.0/illegal_categorys')
		.then(function(response){
			console.log("actions",response);
			commit('loadIllegalCategorys',response.data)
		}).catch(function(error){
			//console.log("actions");
			commit('loadIllegalCategorys',response.data)
		})
    },
	loadLeaveSystememp ({ commit, state }) {
		if (!state.isLSempLoad){
			axios.get('/kong/leave_system/v1.0/illegal_categorys')
			.then(function(response){
				commit('loadLeaveSystememp',response.data)
			}).catch(function(error){
				//console.log("actions");
				commit('loadLeaveSystememp',response.data)
			})
		}
    },
	loadLpillegalCategory ({ commit, state },data) {
		axios.get('/kong/gongdi_mng/v1.0/illegal_categorys_lk',{params: data})
		.then(function(response){
			console.log("actions",response);
			commit('loadillegalCategory',response.data)
		}).catch(function(error){
			//console.log("actions");
			commit('loadillegalCategory',response.data)
		})
    },
	loadMlillegalCategory ({ commit, state },data) {   
		axios.get('/kong/leave_system/v1.0/company/'+data+'/illegalCategory',)
		.then(function(response){
			console.log("actions",response);
			commit('loadMlillegalCategory',response.data)
		}).catch(function(error){
			//console.log("actions");
			commit('loadMlillegalCategory',response.data)
		})
    },
	getillegalCategory ({ commit, state }) {
		axios.get('/kong/gongdi_mng/v1.0/illegal_categorys')
		.then(function(response){
			console.log("actions",response);
			commit('loadillegalCategory',response.data)
		}).catch(function(error){
			console.log(error);
			commit('loadillegalCategory',response.data)
		})
    },
	saveIllegalCategorys({ commit,state},data){	
		if (state.actionStatus==1){  // insert
			state.waitcomplete=true;
			axios.post('/kong/gongdi_mng/v1.0/illegal_categorys',data)
			.then(function(response){
				commit('insertedIllegalCategory',{isSuccess:true,data:response.data});
			}).catch(function(error){
				commit('insertedIllegalCategory',{isSuccess:false})
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
				axios.put('/kong/gongdi_mng/v1.0/illegal_categorys/'+data['id'],modify)
				.then(function(response){
					commit('editedIllegalCategory',{isSuccess:true,data:response.data});
				}).catch(function(error){
					commit('editedIllegalCategory',{isSuccess:false})
				})  
			}else{
				state.actionStatus=0;
				state.active=null;
				state.waitcomplete=false;
			}
		}else if (state.actionStatus==3){  //delete
			axios.delete('/kong/gongdi_mng/v1.0/illegal_categorys/'+state.active['id'])
			.then(function(response){
				commit('deleteedIllegalCategory',{isSuccess:true});
			}).catch(function(error){
				commit('deleteedIllegalCategory',{isSuccess:false})
			})
		}
	},
	editIllegalCategorys({ commit,state},{id}){
		commit('setIllegalCategoryActive',{id:id});
		commit('editingIllegalCategory');
	},
	removeIllegalCategorys({dispatch,commit,state},{id}){
		commit('setIllegalCategoryActive',{id:id});
		commit('deleteingIllegalCategory');
		dispatch('saveIllegalCategorys',{});
	},
}

// mutations 修改 state
const mutations = {
	setissuccess(state,data){
		state.issuccess=true;
		console.log(state.issuccess);
    },
    loadIllegalCategorys(state,data){
        //state.illegalCategorydata=data;
		state.datas=data;
		state.total=data.total
    },
	loadMlillegalCategory(state,data){
		state.MLempdatas=data;		
    },
	resetillegal_category(state){
        //state.illegalCategorydata=data;
		state.datas=[];
		//state.isLoad=false;
    },
	insertingIllegalCategory(state,data){
		state.actionStatus=1;
    },
	insertedIllegalCategory(state,{isSuccess,data}){
		state.waitcomplete=false;
		if (isSuccess){
			state.datas.push(data);
			state.active=null;
			state.actionStatus=0;
		}else{
			state.actionStatus=1;
		}
	},
	editingIllegalCategory(state,data){
		state.actionStatus=2;//edit
    },
	editedIllegalCategory(state,{isSuccess,data}){
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
	deleteingIllegalCategory(state){
		state.actionStatus=3;
	},
	deleteedIllegalCategory(state,{isSuccess}){
		if (isSuccess){
			state.datas=state.datas.filter(item =>item.id!=state.active['id']);
			state.actionStatus=0;
			state.active=null;
		}else{
			state.actionStatus=3;
		}
	},
	cancleIllegalCategorys(state){
		state.active=null;
		state.actionStatus=0;
	},
	setIllegalCategoryActive(state,{id}){
		state.active=state.datas.find(item =>item.id==id);
		//console.log(id);
	},
}

export default {
    state,
    getters,
    actions,
    mutations
}