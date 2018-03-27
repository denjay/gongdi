import axios from 'axios'

const state = ()=>{
    return {dantis: [],companies:[]}
}

const getters = {
    dantis:state=>{
		return state.dantis;
    },
    companies:state=>{
        return state.companies
    }
}

const mutations = {
    setCompanyid(state, data){
        state.companyid = data
    },
    setDantis(state, data){
        state.dantis = data
    },
    removeDanti(state,data){
        var index = state.dantis.indexOf(data)
        state.dantis.splice(index,1)
    },
    setCompanies(state,data){
        state.companies = data
    }
}

const actions = {
    getCompanies({commit}){
        axios.get('/kong/employeemng/v1.0/companys')
        .then(response=>{
            if(response.status === 200){
                commit('setCompanies',response.data)
            }
        })
    },
    getDantis({commit},data){
        axios.get(`/kong/gongdi_mng/v1.0/company/${data}/dantis`)
		.then(function(response){
            commit('setDantis',response.data)
            console.log("actions",response);
		}).catch(function(error){
			console.log("actions");
		})
    },
    postDantis({commit, getters},data){
        axios.post('/kong/gongdi_mng/v1.0/dantis',data)
		.then(response => {
            if (response.status === 201) {
                data = getters.dantis 
                data.unshift(response.data)
                commit('setDantis', data)
                // alert('新增成功！')
            }
            else {
                alert('新增失败')
            }
		}).catch(function(error){
			alert('请求失败')
		})
    },
    putDantis({commit,getters},data){
        delete data.comp_name
        delete data.dantiid
        axios.put(`/kong/gongdi_mng/v1.0/dantis/${data.id}`,data)
        .then(response => {
            if(response.status === 201){
                for(var item of getters.dantis){
                    if(item.id === data.id){
                        var index = getters.dantis.indexOf(item)
                        var [...newDatas] = getters.dantis
                        newDatas.splice(index, 1, response.data)
                        commit('setDantis',newDatas)
                        break
                    }
                }
            }
        })
        .catch(error => {
            alert('出错')
        })
    },
    removeDantis({commit},data){
        axios.delete(`/kong/gongdi_mng/v1.0/dantis/${data.id}`)
			.then(function(response){
                if(response.status === 204){
                    commit('removeDanti',data)
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