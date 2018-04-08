import axios from 'axios'
import buwei from './buwei'

// const doc_map = {"guifang":"Guifangs","tuzhi":"Tuzhis","tuji":"Tujis"}

const state = ()=>{
    return {
        guifangs:[],
        tuzhis:[],
        tujis:[],
        guifang_total_pages:null,
        tuzhi_total_pages:null,
        tuji_total_pages:null
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
    },
    guifang_total_pages:state=>{
        return state.guifang_total_pages
    },
    tuzhi_total_pages:state=>{
        return state.tuzhi_total_pages
    },
    tuji_total_pages:state=>{
        return state.tuji_total_pages
    },
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
    },
    setGuifangTotalPages(state, data){
        state.guifang_total_pages = data
    },
    setTuzhiTotalPages(state, data){
        state.tuzhi_total_pages = data
    },
    setTujiTotalPages(state, data){
        state.tuji_total_pages = data
    }
}

const actions = {
    getDocs({commit},data){
        var doc_types = data.doc_types
        delete data.doc_types

        var query_args = ''
        for(var key in data){
            if(Boolean(data[key])){
                query_args += `&${key}=${data[key]}`
            }
        }
        for(var doc_type of doc_types){
            axios.get(`/kong/gongdi_mng/v1.0/${doc_type}_docs?${query_args}`,{doc_type})
            .then(response=>{
                if(response.status === 200){
                    // 增加doc_type字段
                    var [...data] = response.data
                    for(var doc of data){
                        doc["doc_type"] = response.config.doc_type
                    }
                    var commit_method = `set_${response.config.doc_type}s`.replace(/_(\w)/g, (x)=>{return x.slice(1).toUpperCase()})
                    commit(commit_method,data)
                    // 获取数据条数
                    var total = response.headers["x-total"]       
                    commit_method = `set_${response.config.doc_type}_total_pages`.replace(/_(\w)/g, (x)=>{return x.slice(1).toUpperCase()})
                    commit(commit_method,total)
                }
            }).catch(function(error){
                alert('getDocs失败')
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
                var {...respData} = response.data
                respData["doc_type"] = doc_type
                docs.unshift(respData)
                var commit_method = `set_${doc_type}s`.replace(/_(\w)/g, (x)=>{return x.slice(1).toUpperCase()})                
                commit(commit_method, docs)
            }
		}).catch(function(error){
			alert('postDocs失败')
		})
    },
    putDocs({commit,getters},data){
        var doc_type = data.doc_type
        delete data.doc_type
        axios.put(`/kong/gongdi_mng/v1.0/${doc_type}_docs/${data.id}`,data)
        .then(response => {
            if(response.status === 201){
                for(var item of getters[`${doc_type}s`]){
                    if(item.id === data.id){
                        var index = getters[`${doc_type}s`].indexOf(item)
                        var [...docs] = getters[`${doc_type}s`]
                        var {...doc} = response.data
                        doc["doc_type"] = doc_type
                        docs.splice(index, 1, doc)
                        var commit_method = `set_${doc_type}s`.replace(/_(\w)/g, (x)=>{return x.slice(1).toUpperCase()})                                        
                        commit(commit_method,docs)
                        break
                    }
                }
            }
        })
        .catch(error => {
            alert('putDocs出错')
        })
    },
    removeDocs({commit},data){
        axios.delete(`/kong/gongdi_mng/v1.0/${data.doc_type}_docs/${data.id}`)
        .then(function(response){
            if(response.status === 204){
                var commit_method = `remove_${data.doc_type}s`.replace(/_(\w)/g, (x)=>{return x.slice(1).toUpperCase()})                                                            
                commit(commit_method,data)
            }
        })
        .catch(function(error){
            alert('removeDocs出错')
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