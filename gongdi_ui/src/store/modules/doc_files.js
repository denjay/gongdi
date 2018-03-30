import axios from 'axios'
import buwei from './buwei'

const state = ()=>{
    return {doc_files:[],docs:[]}
}

const getters = {
    doc_files:state=>{
        return state.doc_files
    },
    docs:state=>{
        return state.docs
    }
}

const  mutations = {
    setDocs(state, data){
        state.docs = data
    },
    setDocFiles(state, data){
        state.doc_files = data
    },
    removeDocFiles(state,data){
        var index = state.doc_files.indexOf(data)
        state.doc_files.splice(index,1)
    },
}

const actions = {
    getDocs({commit,getters},buweiid){
        axios.get(`/kong/gongdi_mng/v1.0/buwei/${buweiid}/jishu_docs`)
        .then(response=>{
            if(response.status === 200){
                commit('setDocs',response.data)
            }
        })
    },
    getDocFiles({commit},docsid){
        axios.get(`/kong/gongdi_mng/v1.0/docs/${docsid}/files`)
        .then(response=>{
            if(response.status === 200){
                commit('setDocFiles',response.data)
            }
        })
    },
    postDocFiles({commit,getters},data){
        axios.post('/kong/gongdi_mng/v1.0/doc_files',data)
		.then(response => {
            if (response.status === 201) {
                var [...doc_files] = getters.doc_files 
                doc_files.unshift(response.data)
                commit('setDocFiles', doc_files)
            }
		}).catch(function(error){
			alert('请求失败')
		})
    },
    putDocFiles({commit,getters},data){
        axios.put(`/kong/gongdi_mng/v1.0/doc_files/${data.id}`,data)
        .then(response => {
            if(response.status === 201){
                for(var item of getters.doc_files){
                    if(item.id === data.id){
                        var index = getters.doc_files.indexOf(item)
                        var [...doc_files] = getters.doc_files
                        doc_files.splice(index, 1, response.data)
                        commit('setDocFiles',doc_files)
                        break
                    }
                }
            }
        })
        .catch(error => {
            alert('出错')
        })
    },
    removeDocFiles({commit},data){
        axios.delete(`/kong/gongdi_mng/v1.0/doc_files/${data.id}`)
			.then(function(response){
                if(response.status === 204){
                    commit('removeDocFiles',data)
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