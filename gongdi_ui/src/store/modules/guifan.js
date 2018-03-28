import axios from 'axios'
import buwei from './buwei'

const state = ()=>{
    return {guifans:[]}
}

const getters = {
    guifans:state=>{
        return state.guifans
    }
}

const  mutations = {
    setGuifans(state, data){
        state.guifans = data
    },
    removeGuifans(state,data){
        var index = state.guifans.indexOf(data)
        state.guifans.splice(index,1)
    },
}

const actions = {
    getGuifans({commit},data){
        var query_args = ''
        for(var key in data){
            if(Boolean(data[key])){
                query_args += `&${key}=${data[key]}`
            }
        }
        axios.get(`/kong/gongdi_mng/v1.0/guifang_docs?${query_args}`)
        .then(response=>{
            if(response.status === 200){
                commit('setGuifans',response.data)
            }
        })
    },
    postGuifans({commit,getters},data){
        axios.post('/kong/gongdi_mng/v1.0/guifang_docs',data)
		.then(response => {
            if (response.status === 201) {
                data = getters.guifans 
                data.unshift(response.data)
                commit('setGuifans', data)
            }
            else {
                alert('新增失败')
            }
		}).catch(function(error){
			alert('请求失败')
		})
    },
    putGuifans({commit,getters},data){
        axios.put(`/kong/gongdi_mng/v1.0/guifang_docs/${data.id}`,data)
        .then(response => {
            if(response.status === 201){
                for(var item of getters.guifans){
                    if(item.id === data.id){
                        var index = getters.guifans.indexOf(item)
                        var [...newDatas] = getters.guifans
                        newDatas.splice(index, 1, response.data)
                        commit('setGuifans',newDatas)
                        break
                    }
                }
            }
        })
        .catch(error => {
            alert('出错')
        })
    },
    removeGuifans({commit},data){
        axios.delete(`/kong/gongdi_mng/v1.0/guifang_docs/${data.id}`)
			.then(function(response){
                if(response.status === 204){
                    commit('removeGuifans',data)
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