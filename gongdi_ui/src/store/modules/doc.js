import axios from 'axios'
import buwei from './buwei'
import doc_files from './doc_files'

const state = ()=>{
    return {
        docs:[],
        total_datas:null,
    }
}

const getters = {
    docs:state=>{
        return state.docs
    },
    total_datas:state=>{
        return state.total_datas
    },
}

const  mutations = {
    setDocs(state, data){
        state.docs = data
    },
    removeDocs(state,data){
        var index = state.docs.indexOf(data)
        state.docs.splice(index,1)
    },
    setTotalDatas(state, data){
        state.total_datas = data
    },
}

const actions = {
    getDocs({commit},data){
        var doc_type = data.doc_type
        delete data.doc_type

        var query_args = ''
        for(var key in data){
            if(Boolean(data[key])){
                query_args += `&${key}=${data[key]}`
            }
        }
        axios.get(`/kong/gongdi_mng/v1.0/${doc_type}_docs?${query_args}`)
        .then(response=>{
            if(response.status === 200){
                // 增加doc_type字段
                var [...data] = response.data
                for(var doc of data){
                    doc["doc_type"] = doc_type
                }
                commit('setDocs',data)
                // 获取数据条数
                var total = response.headers["x-total"]       
                commit('setTotalDatas',total)
            }
        })
        .catch(function(error){
            alert('getDocs失败')
        })
    },
    postDocs({commit,getters},data){
        var doc_type = data.doc_type
        delete data.doc_type
        axios.post(`/kong/gongdi_mng/v1.0/${doc_type}_docs`,data)
		.then(response => {
            if (response.status === 201) {
                var [...docs] = getters["docs"] 
                var {...respData} = response.data
                respData["doc_type"] = doc_type
                docs.unshift(respData)
                commit('setDocs', docs)
            }
        })
        .catch(function(error){
			alert('postDocs失败')
		})
    },
    putDocs({commit,getters},data){
        var doc_type = data.doc_type
        delete data.doc_type
        axios.put(`/kong/gongdi_mng/v1.0/${doc_type}_docs/${data.id}`,data)
        .then(response => {
            if(response.status === 201){
                var [...docs] = getters["docs"]
                for(var item of docs){
                    if(item.id === data.id){
                        var index = docs.indexOf(item)
                        var {...doc} = response.data
                        doc["doc_type"] = doc_type
                        docs.splice(index, 1, doc)
                        commit('setDocs',docs)
                        break
                    }
                }
            }
        })
        .catch(error => {
            alert('putDocs出错')
        })
    },
    removeDocs({commit,dispatch},data){
        axios.delete(`/kong/gongdi_mng/v1.0/${data.doc_type}_docs/${data.id}`)
        .then(function(response){
            if(response.status === 204){
                dispatch("getDocs",data["query_args"])
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
    modules:{buwei,doc_files}
}