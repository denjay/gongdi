<template>
  <div>
    <div class="">
      <div class="select">
        <span>选择公司：</span>
        <el-select v-model="companyid" filterable clearable placeholder="请选择公司">
          <el-option
            v-for="company in companies"
            :key="company.id"
            :label="company.company_name"
            :value="company.id">
          </el-option>
        </el-select>
        <br>
        <span>选择单体：</span>        
        <el-select v-model="dantiid" filterable clearable placeholder="请选择单体">
          <el-option
            v-for="danti in dantis"
            :key="danti.id"
            :label="danti.name"
            :value="danti.id">
          </el-option>
        </el-select>
        <br>
        <span>选择部位：</span>
        <el-select v-model="buweiid" filterable clearable placeholder="请选择部位">
          <el-option
            v-for="buwei in buweis"
            :key="buwei.id"
            :label="buwei.name"
            :value="buwei.id">
          </el-option>
        </el-select>
        <br>
        <span>文档类型：</span>
        <el-select v-model="doc_type" filterable clearable placeholder="请选择文档类型">
          <el-option
            v-for="(val,key,index) in doc_types"
            :key="index"
            :label="key"
            :value="val">
          </el-option>
        </el-select>
        <br>
        <span>选择文档：</span>
        <el-select v-model="docsid" filterable clearable placeholder="请选择文档">
          <el-option
            v-for="val in docs[doc_type]"
            :key="val.index"
            :label="val.name"
            :value="val.id">
          </el-option>
        </el-select>
      </div>
      <br>
      <el-button @click="getDocFiles" :disabled="!docsid" type="primary">查询文档附件</el-button>
      <el-button @click="insert" type="primary">新增文档附件</el-button>
    </div>

    <el-table
      :data="doc_files"
      border
      style="width: 100%">
      <el-table-column
        fixed
        prop="id"
        label="id"
        width="100">
      </el-table-column>
      <el-table-column
        prop="file_size"
        width="150"
        label="文件大小(kb)">
      </el-table-column>
      <el-table-column
        prop="file_name"
        label="文件名">
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作"
        width="100">
        <template slot-scope="scope">
          <el-button @click="remove(scope.row)" type="text" size="mini" icon="el-icon-delete"></el-button>
          <el-button @click="edit(scope.row)" type="text" size="mini" icon="el-icon-edit"></el-button>
          <a :href="`/kong/gongdi_mng/v1.0/doc_files/${data.id}`"></a>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">
      <el-form label-position="right" label-width="100px">
        <template v-if="title === '新增文档附件'">
          <el-form-item label="公司名称">
            <el-select v-model="companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属单体">
            <el-select v-model="dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属部位">
            <el-select v-model="buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
          </el-form-item>
        </template>
        <el-form-item label="文件">
          <el-upload
            class="upload-demo"
            action="/kong/gongdi_mng/v1.0/doc_files"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            multiple
            :limit="3"
            :on-exceed="handleExceed"
            :file-list="fileList">
            <el-button size="small" type="primary">点击上传</el-button>
            <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
          </el-upload>
        </el-form-item>        
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitData">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
  import axios from 'axios'  
  import {mapGetters} from 'vuex'
  export default {
    mounted(){
      this.$store.dispatch('doc_files/buwei/getCompanies')
    },

    data() {
      return {
        companyid: '',
        dantiid: '',
        buweiid: null,
        doc_type: '',
        doc_types: {"规范":"guifang_doc","图纸":"tuzhi_doc","图集":"tuji_doc","交底":"jiaodi_doc"},
        docsid: null,
        file_name: '',
        file_size: null,
        // file_id: null,
        fileList:[],
        dialogVisible: false,
        title: '',
      }
    },

    methods: {
      getDocFiles(){
        this.$store.dispatch('doc_files/getDocFiles', this.docsid)        
      },
      download(data){
        axios.get(`/kong/gongdi_mng/v1.0/doc_files/${data.id}`)
        // .then(response=>{
        //     if(response.status === 200){
        //         commit('setDocFiles',response.data)
        //     }
        // })
      },
      insert(){
        // 新增时先清空表单数据        
        this.title = '新增文档附件'
        this.dialogVisible = true
        this.docsid = ''
        this.name = ''
        this.description = ''
      },
      edit(data){
        // 点编辑时，将对应行数据写入表单        
        this.title = '编辑文档附件'
        this.docsid = data.id
        this.name = data.name
        this.dialogVisible = true
      },
      submitData(){
        // 组织表单需要的数据，创建或更新数据        
        var data = {
          name:this.name,
          docsid:this.docsid,
        }
        if(!Boolean(data.jiaodi_time)){
          delete data.jiaodi_time
        }
        else{
          // 解决时间格式不对的问题
          data.jiaodi_time = new Date(data.jiaodi_time)
        }
        if(this.title === '新增文档附件'){
          this.$store.dispatch('doc_files/postJiaodis',data)
        }
        else if(this.title === '编辑文档附件'){
          data["id"] = this.docsid
          delete data.buweiid          
          this.$store.dispatch('doc_files/putJiaodis',data)
        }
        this.dialogVisible = false
      },
      remove(data) {
        this.$confirm('此操作將永久刪除該資料, 是否繼續?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
        }).then(() => {
          this.$store.dispatch('doc_files/removeJiaodis',data);
        }).catch(() => {         
        });
      },
      handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
          .catch(_ => {});
      },
      // upload相关
      handleRemove(file, fileList) {
        console.log(file, fileList);
      },
      handlePreview(file) {
        console.log(file);
      },
      handleExceed(files, fileList) {
        this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
      },
      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${ file.name }？`);
      }
    },

    computed: {
      buwei_name(){
        if(Boolean(this.buweiid)){
          return this.buweis.filter(item => item.id === this.buweiid)[0]["name"]
        }
      },
      ...mapGetters('doc_files/buwei',{
        'dantis':'dantis',
        'companies':'companies',
        'buweis':'buweis',
        }
      ),
      ...mapGetters('doc_files',{
        'doc_files':'doc_files',
        'docs':'docs',
		  }),
    },

    watch:{
      companyid: function(){
        this.dantiid = ''
        this.$store.commit('doc_files/buwei/setDantis',[])
        if(Boolean(this.companyid)){
          this.$store.dispatch('doc_files/buwei/getDantis', this.companyid)
        }
      },
      dantiid: function(){
        this.buweiid = null
        this.$store.commit('doc_files/buwei/setBuweis',[])
        if(Boolean(this.dantiid)){
          this.$store.dispatch('doc_files/buwei/getBuweis', this.dantiid)
        }
      },
      buweiid: function(){
        this.docsid = null
        this.$store.commit('doc_files/setDocs',[])
        if(Boolean(this.buweiid)){
          this.$store.dispatch('doc_files/getDocs', this.buweiid)
        }
      },
      doc_type: function(){
        this.docsid = null
        this.$store.commit('doc_files/setDocs',[])
        if(Boolean(this.buweiid)){
          this.$store.dispatch('doc_files/getDocs', this.buweiid)
        }
      },
    }     
  }
</script>

<style scoped>
  .select span {
    display:inline-block;
    width: 70px;
    font-size: 13px;
  }
  .el-select {
    width: 200px;
    margin-bottom: 20px;
  }
  .select {
    width: 700px;
    margin-right: 20px;
    display: inline-block;
  }
  .el-input {
    width: 200px;
    margin-bottom: 20px;
  }
  .el-form-item {
    margin-bottom: 0px;
  }
  .el-textarea {
    width: 200px;
  }
</style>

<style>
  .el-dialog {
    width: 385px !important;
  }
  .el-table {
    margin-top: 5px;
  }
</style>
