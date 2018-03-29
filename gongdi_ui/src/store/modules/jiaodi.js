import axios from 'axios'
import buwei from './buwei'

const state = ()=>{
    return {jiaodis:[]}
}

const getters = {
    jiaodis:state=>{
        return state.jiaodis
    }
}

const  mutations = {
    setJiaodis(state, data){
        state.jiaodis = data
    },
    removeJiaodis(state,data){
        var index = state.jiaodis.indexOf(data)
        state.jiaodis.splice(index,1)
    },
}

const actions = {
    getJiaodis({commit},data){
        var query_args = ''
        for(var key in data){
            if(Boolean(data[key])){
                query_args += `&${key}=${data[key]}`
            }
        }
        axios.get(`/kong/gongdi_mng/v1.0/jiaodi_docs?${query_args}`)
        .then(response=>{
            if(response.status === 200){
                commit('setJiaodis',response.data)
            }
        })
    },
    postJiaodis({commit,getters},data){
        axios.post('/kong/gongdi_mng/v1.0/jiaodi_docs',data)
		.then(response => {
            if (response.status === 201) {
                var [...jiaodi] = getters.jiaodis 
                jiaodi.unshift(response.data)
                commit('setJiaodis', jiaodi)
            }
		}).catch(function(error){
			alert('请求失败')
		})
    },
    putJiaodis({commit,getters},data){
        axios.put(`/kong/gongdi_mng/v1.0/jiaodi_docs/${data.id}`,data)
        .then(response => {
            if(response.status === 201){
                for(var item of getters.jiaodis){
                    if(item.id === data.id){
                        var index = getters.jiaodis.indexOf(item)
                        var [...jiaodis] = getters.jiaodis
                        jiaodis.splice(index, 1, response.data)
                        commit('setJiaodis',jiaodis)
                        break
                    }
                }
            }
        })
        .catch(error => {
            alert('出错')
        })
    },
    removeJiaodis({commit},data){
        axios.delete(`/kong/gongdi_mng/v1.0/jiaodi_docs/${data.id}`)
			.then(function(response){
                if(response.status === 204){
                    commit('removeJiaodis',data)
                }
			}).catch(function(error){
			})
    }
}

export default {
    namespaced: true,    
    state,
    getters,
    mutations,
    actions,
    modules:{buwei}
}