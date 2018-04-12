import axios from 'axios';
const state = {
    datas:[],
	total:0,
	LSempdatas:[],
	subcontractorlks:[],
	loadfilter:{
		page:0,
		per_page:0,
		comp_name:'',
		manager:'',
	},
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
    subcontractors:state=>{
		return state.datas;
    },
	subcontractorlks:state=>{
		return state.subcontractorlks;
    },
	subcontractorstotal:state=>{
		return state.total;
    },
	LSsubcontractors:state=>{
		return state.LSempdatas;
    },
	subcontractorsActionStatus:state=>{
		return state.actionStatus;
    },
	waitsubcstatus:state=>{
		return state.waitcomplete;
    },
}

// actions
const actions = {
	loadSubcontractors ({ commit, state },data) {
		if (!(state.loadfilter.page==data.page&&
				state.loadfilter.per_page==data.per_page&&
				state.loadfilter.comp_name==data.comp_name&&
				state.loadfilter.manager==data.manager
			)){
			axios.get('/kong/gongdi_mng/v1.0/subcontractors',{params: data})
			.then(function(response){
				state.loadfilter.page=data.page;
				state.loadfilter.per_page=data.per_page;
				state.loadfilter.comp_name=data.comp_name;
				state.loadfilter.manager=data.manager;
				commit('loadSubcontractors',response)
			}).catch(function(error){
				//console.log("actions");
				commit('loadSubcontractors',response)
			})
		}
    },  
	loadSubcontractorLks ({ commit, state }) {
		axios.get('/kong/gongdi_mng/v1.0/subcontractors')
		.then(function(response){
			commit('loadSubcontractorLks',response.data)
		}).catch(function(error){
			console.log(error);
			commit('loadSubcontractorLks',response.data)
		})
    },
	saveSubcontractors({ commit,state},data){	
		if (state.actionStatus==1){  // insert
			state.waitcomplete=true;
			axios.post('/kong/gongdi_mng/v1.0/subcontractors',data)
			.then(function(response){
				commit('insertedSubcontractors',{isSuccess:true,data:response.data});
			}).catch(function(error){
				commit('insertedSubcontractors',{isSuccess:false})
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
				axios.put('/kong/gongdi_mng/v1.0/subcontractors/'+data['id'],modify)
				.then(function(response){
					commit('editedSubcontractors',{isSuccess:true,data:response.data});
				}).catch(function(error){
					commit('editedSubcontractors',{isSuccess:false})
				})  
			}else{
				state.actionStatus=0;
				state.active=null;
				state.waitcomplete=false;
			}
		}else if (state.actionStatus==3){  //delete
			axios.delete('/kong/gongdi_mng/v1.0/subcontractors/'+state.active['id'])
			.then(function(response){
				commit('deleteedSubcontractors',{isSuccess:true});
			}).catch(function(error){
				commit('deleteedSubcontractors',{isSuccess:false})
			})
		}
	},
	editSubcontractors({ commit,state},{id}){
		commit('setSubcontractorsActive',{id:id});
		commit('editingSubcontractors');
	},
	removeSubcontractors({dispatch,commit,state},{id}){
		commit('setSubcontractorsActive',{id:id});
		commit('deleteingSubcontractors');
		dispatch('saveSubcontractors',{});
	},
}

// mutations 修改 state
const mutations = {
	setissuccess(state,data){
		state.issuccess=true;
		console.log(state.issuccess);
    },
    loadSubcontractors(state,data){
		state.datas=data.data;
		state.total=parseInt(data.headers['x-total']);
    },
	loadSubcontractorLks(state,data){
		state.subcontractorlks=data;		
    },
	resetemp(state){
        //state.employeedata=data;
		state.datas=[];
		state.loadfilter={
			page:0,
			per_page:0,
			comp_name:'',
			manager:'',
		}
    },
	insertingSubcontractors(state,data){
		state.actionStatus=1;
    },
	insertedSubcontractors(state,{isSuccess,data}){
		state.waitcomplete=false;
		if (isSuccess){
			state.datas.push(data);
			state.active=null;
			state.actionStatus=0;
		}else{
			state.actionStatus=1;
		}
	},
	editingSubcontractors(state,data){
		state.actionStatus=2;//edit
    },
	editedSubcontractors(state,{isSuccess,data}){
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
	deleteingSubcontractors(state){
		state.actionStatus=3;
	},
	deleteedSubcontractors(state,{isSuccess}){
		if (isSuccess){
			state.datas=state.datas.filter(item =>item.id!=state.active['id']);
			state.actionStatus=0;
			state.active=null;
		}else{
			state.actionStatus=3;
		}
	},
	cancleSubcontractors(state){
		state.active=null;
		state.actionStatus=0;
	},
	setSubcontractorsActive(state,{id}){
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