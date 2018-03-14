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
    },
    removeDanti(state,data){
        var index = state.datas.indexOf(data)
        state.datas.splice(index,1)
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
        axios.post('/kong/gongdi_mng/v1.0/dantis',data)
		.then(response => {
            if (response.status === 201) {
                context.commit('setDantis', data)
                alert('新增成功！')
            }
            else {
                alert('新增失败')
            }
            console.log("actions",response);
		}).catch(function(error){
			alert('请求失败')
		})
    },
    removeDantis(context,data){
        axios.delete(`http://127.0.0.1:8889/gongdi_mng/v1.0/dantis/${data.id}`)
			.then(function(response){
                if(response.status === 204){
                    context.commit('removeDanti',data)
                }
			}).catch(function(error){
			})
    }
}

export default {
    state,
    getters,
    mutations,
    actions
}