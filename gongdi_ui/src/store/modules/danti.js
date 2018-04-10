import axios from 'axios'

const state = ()=>{
    return {dantis: [],companies:[],total_datas:null}
}

const getters = {
    dantis:state=>{
		return state.dantis;
    },
    companies:state=>{
        return state.companies
    },
    total_datas:state=>{
        return state.total_datas
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
    },
    setTotalDatas(state,data){
        state.total_datas = data
    },
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
        var companyid = data["companyid"]
        delete data["companyid"]
        var query_args = "?"
        for(var key in data){
            if(Boolean(data[key])){
                query_args = `${query_args}&${key}=${data[key]}`
            }
        }
        axios.get(`/kong/gongdi_mng/v1.0/company/${companyid}/dantis${query_args}`)
		.then(function(response){
            commit('setDantis',response.data)
            // 获取数据条数
            var total = response.headers["x-total"]       
            commit("setTotalDatas",total)
        })
        .catch(function(error){
			alert('getDantis失败')
		})
    },
    postDantis({commit, getters},data){
        axios.post('/kong/gongdi_mng/v1.0/dantis',data)
		.then(response => {
            if (response.status === 201) {
                var dantis = getters.dantis 
                dantis.unshift(response.data)
                commit('setDantis', dantis)
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
            alert('putDantis出错')
        })
    },
    removeDantis({commit},data){
        axios.delete(`/kong/gongdi_mng/v1.0/dantis/${data.id}`)
        .then(function(response){
            if(response.status === 204){
                commit('removeDanti',data)
            }
        })
        .catch(function(error){
            alert('removeDantis出错')
        })
    }
}

export default {
    state,
    getters,
    mutations,
    actions
}