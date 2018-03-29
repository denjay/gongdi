import axios from 'axios'
import buwei from './buwei'

const doc_map = {"guifang":"Guifangs","tuzhi":"Tuzhis","tuji":"Tujis"}

const state = ()=>{
    return {
        guifangs:[],
        tuzhis:[],
        tujis:[],
    }
}

const getters = {
    guifangs:state=>{
        return state.guifangs
    },
    tuzhis:state=>{
        return state.tuzhis
    },
    tujis:state=>{
        return state.tujis
    }
}

const  mutations = {
    setGuifangs(state, data){
        state.guifangs = data
    },
    removeGuifangs(state,data){
        var index = state.guifangs.indexOf(data)
        state.guifangs.splice(index,1)
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
        for(var doc_type in doc_map){
            axios.get(`/kong/gongdi_mng/v1.0/${doc_type}_docs?${query_args}`,{doc_type})
            .then(response=>{
                if(response.status === 200){
                    // 增加doc_type字段
                    var [...data] = response.data
                    for(var doc of data){
                        doc["doc_type"] = response.config.doc_type
                    }
                    commit(`set${doc_map[response.config.doc_type]}`,data)
                }
            })

        }
    },
    postDocs({commit,getters},data){
        var doc_type = data.doc_type
        delete data.doc_type
        axios.post(`/kong/gongdi_mng/v1.0/${doc_type}_docs`,data)
		.then(response => {
            if (response.status === 201) {
                var [...docs] = getters[`${doc_type}s`] 
                docs.unshift(response.data)
                commit(`set${doc_map[doc_type]}`, docs)
            }
		}).catch(function(error){
			alert('请求失败')
		})
    },
    putDocs({commit,getters},data){
        var doc_type = data.doc_type
        delete data.doc_type
        axios.put(`/kong/gongdi_mng/v1.0/${doc_type}_docs/${data.id}`,data)
        .then(response => {
            if(response.status === 201){
                console.log('doc',doc_type,getters[`${doc_type}s`])
                for(var item of getters[`${doc_type}s`]){
                    if(item.id === data.id){
                        var index = getters[`${doc_type}s`].indexOf(item)
                        var [...docs] = getters[`${doc_type}s`]
                        var {...doc} = response.data
                        doc["doc_type"] = doc_type
                        docs.splice(index, 1, doc)
                        commit(`set${doc_map[doc_type]}`,docs)
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
        axios.delete(`/kong/gongdi_mng/v1.0/${data.doc_type}_docs/${data.id}`)
			.then(function(response){
                if(response.status === 204){
                    commit(`remove${doc_map[data.doc_type]}`,data)
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