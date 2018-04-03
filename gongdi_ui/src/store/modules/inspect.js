import axios from 'axios'
import buwei from './buwei'

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
        var index = state.quality_inspects.indexOf(data)
        state.quality_inspects.splice(index,1)
    },
    setSafetyInspects(state, data){
        state.safety_inspects = data
    },
    removeSafetyInspects(state,data){
        var index = state.safety_inspects.indexOf(data)
        state.safety_inspects.splice(index,1)
    },
    setProduceInspects(state, data){
        state.produce_inspects = data
    },
    removeProduceInspects(state,data){
        var index = state.produce_inspects.indexOf(data)
        state.produce_inspects.splice(index,1)
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
                    var newData = response.data
                    var item = {}
                    for(item of newData){
                        item["type"] = response.config.insp_type.slice(0,-1)
                    }
                    commit(insp_methods[response.config.insp_type],newData)
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
		}).catch(function(error){
			alert('请求失败')
		})
    },
    putInspects({commit,getters,dispatch},data){
        var insp_type = data.type
        var id = data.id
        delete data.type
        delete data.id
        axios.put(`/kong/gongdi_mng/v1.0/${insp_type}s/${id}`,data)
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
        var {...data_copy} = data
        var insp_type = data.type
        var id = data.id
        delete data.type
        delete data.id
        axios.delete(`/kong/gongdi_mng/v1.0/${insp_type}s/${id}`)
			.then(function(response){
                if(response.status === 204){
                    var commit_method = `remove_${insp_type}s`
                    // 将下划线式转为驼峰式
                    commit_method = commit_method.replace(/_(\w)/g, (x)=>{return x.slice(1).toUpperCase()})
                    delete data_copy.buweiid
                    delete data_copy.id
                    commit(commit_method,data_copy)
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