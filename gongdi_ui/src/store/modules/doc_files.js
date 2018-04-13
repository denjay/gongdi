import axios from 'axios'

// 以后要把docs部分删掉

const state = ()=>{
    return { doc_files:[], docs:[] }
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
        .catch(function(error){
			alert('getDocs失败')
		})
    },
    getDocFiles({commit},docsid){
        axios.get(`/kong/gongdi_mng/v1.0/docs/${docsid}/files`)
        .then(response=>{
            if(response.status === 200){
                commit('setDocFiles',response.data)
            }
        })
        .catch(function(error){
			alert('getDocFiles失败')
		})
    },
    removeDocFiles({commit},data){
        axios.delete(`/kong/gongdi_mng/v1.0/doc_files/${data.id}`)
        .then(function(response){
            if(response.status === 204){
                commit('removeDocFiles',data)
            }
        })
        .catch(function(error){
            alert('removeDocFiles失败')
        })
    }
}

export default {
    namespaced: true,    
    state,
    getters,
    mutations,
    actions,
}