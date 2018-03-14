import axios from 'axios'

const state = {
    companyid: '',
    datas: []
}

const getters = {
    dantis:state=>{
		return state.datas;
    }
}

const  mutations = {
    setCompanyid(state, data){
        state.companyid = data
    },
    setDantis(state, data){
        state.datas = data
    }
}

const actions = {
    getDantis(context){
        axios.get(`/kong/gongdi_mng/v1.0/company/${context.state.companyid}/dantis`)
		.then(function(response){
            context.commit('setDantis',response.data)
            // alert(context.state.tableDatas);
            console.log("actions",response);
		}).catch(function(error){
			console.log("actions");
			// commit('loadMlillegalCategory',response.data)
		})
    },
    postDantis(context,data){
        axios.post(`/kong/gongdi_mng/v1.0/dantis`,data)
		.then(response => {
            if (response.status === 201) {
                context.commit('setDantis', data)
                alert('新增成功！')
            }
            else {
                alert('新增失败')
            }
            context.commit('setDantis',response.data)
            // alert(context.state.tableDatas);
            console.log("actions",response);
		}).catch(function(error){
			console.log("actions");
			// commit('loadMlillegalCategory',response.data)
		})
    }
}

export default {
    state,
    getters,
    mutations,
    actions
}