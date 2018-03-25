import axios from 'axios'

const state = {
    quality_inspects:[],
    safety_inspects:[],
    produce_inspects:[],
}

const getters = {
    quality_inspects:state=>{
        return state.quality_inspects
    },
    safety_inspects:state=>{
        return state.safety_inspects
    },
    produce_inspects:state=>{
        return state.produce_inspects
    }
}

const  mutations = {
    setQualityInspects(state, data){
        state.quality_inspects = data
    },
    removeQualityInspects(state,data){
        var index = state.QualityInspects.indexOf(data)
        state.QualityInspects.splice(index,1)
    },
    setSafetyInspects(state, data){
        state.safety_inspects = data
    },
    removeSafetyInspects(state,data){
        var index = state.SafetyInspects.indexOf(data)
        state.SafetyInspects.splice(index,1)
    },
    setProduceInspects(state, data){
        state.produce_inspects = data
    },
    removeProduceInspects(state,data){
        var index = state.ProduceInspects.indexOf(data)
        state.ProduceInspects.splice(index,1)
    },
}

const actions = {
    getInspects({commit},data){
        var insp_methods = {
            "quality_inspects":"setQualityInspects", 
            "safety_inspects":"setSafetyInspects", 
            "produce_inspects":"setProduceInspects"
            }
        var path = ''
        for(var insp_type in insp_methods){
            path = insp_type + '?'
            for(var key in data){
                if(Boolean(data[key])){
                    path =  `${path}&${key}=${data[key]}`
                }
            }
            axios.get(`/kong/gongdi_mng/v1.0/${path}`,{'insp_type':insp_type})
            .then(response=>{
                if(response.status === 200){
                    commit(insp_methods[response.config.insp_type],response.data)
                }
            })
        }
    },
    postInspects({commit,getters,dispatch},data){
        var insp_type = data.type
        delete data.type
        axios.post(`/kong/gongdi_mng/v1.0/${insp_type}s`,data,{insp_type})
		.then(response => {            
            if (response.status === 201) {
                var newData = {buweiid:data.buweiid,insp_date:data.insp_date,insp_emp:data.insp_emp}
                dispatch('getInspects',newData)
            }
            else {
                alert('新增失败')
            }
		}).catch(function(error){
			alert('请求失败')
		})
    },
    putInspects({commit,getters},data){
        var insp_type = data.type
        var id = data.id
        delete data.type
        delete data.id
        axios.put(`/kong/gongdi_mng/v1.0/${insp_type}/${id}`,data)
        .then(response => {
            if(response.status === 201){
                var newData = {buweiid:data.buweiid,insp_date:data.insp_date,insp_emp:data.insp_emp}
                dispatch('getInspects',newData)
            }
        })
        .catch(error => {
            alert('出错')
        })
    },
    removeInspects({commit},data){
        var insp_type = data.type
        var id = data.id
        delete data.type
        delete data.id
        axios.delete(`/kong/gongdi_mng/v1.0/${insp_type}/${id}`)
			.then(function(response){
                if(response.status === 204){
                    // commit('removeBuweis',data)
                }
			}).catch(function(error){
			})
    }
}

export default {
    state,
    getters,
    mutations,
    actions
}