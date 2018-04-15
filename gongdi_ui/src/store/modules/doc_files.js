import axios from 'axios'

const state = ()=>{
    return { doc_files:[] }
}

const getters = {
    doc_files:state=>{
        return state.doc_files
    },
}

const  mutations = {
    setDocFiles(state, data){
        state.doc_files = data
    },
    removeDocFiles(state,data){
        var index = state.doc_files.indexOf(data)
        state.doc_files.splice(index,1)
    },
}

const actions = {
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