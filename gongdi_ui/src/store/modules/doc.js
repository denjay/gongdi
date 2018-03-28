import axios from 'axios'
import buwei from './buwei'

const state = ()=>{
    return {
        guifans:[],
        tuzhis:[],
        tujis:[],
    }
}

const getters = {
    guifans:state=>{
        return state.guifans
    },
    tuzhis:state=>{
        return state.tuzhis
    },
    tujis:state=>{
        return state.tujis
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
    setTuzhis(state, data){
        state.tuzhis = data
    },
    removeTuzhis(state,data){
        var index = state.tuzhis.indexOf(data)
        state.tuzhis.splice(index,1)
    },
    setTujis(state, data){
        state.tujis = data
    },
    removeTujis(state,data){
        var index = state.tujis.indexOf(data)
        state.tujis.splice(index,1)
    }
}

const actions = {
    getDocs({commit},data){
        var query_args = ''
        for(var key in data){
            if(Boolean(data[key])){
                query_args += `&${key}=${data[key]}`
            }
        }
        var doc_map = {"guifang":"Guifans","tuzhi":"Tuzhis","tuji":"Tujis"}
        for(var doc_type in doc_map){
            axios.get(`/kong/gongdi_mng/v1.0/${doc_type}_docs?${query_args}`,{doc_type})
            .then(response=>{
                if(response.status === 200){
                    commit(`set${doc_map[response.config.doc_type]}`,response.data)
                }
            })

        }
    },
    postDocs({commit,getters},data){
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
    putDocs({commit,getters},data){
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
    removeDocs({commit},data){
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