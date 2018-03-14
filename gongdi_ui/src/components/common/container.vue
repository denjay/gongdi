<template>
	<el-tabs v-model="editableTabsValue" type="border-card" closable @tab-click="locationsider" 
		@tab-remove="removeone" style="margin:0px 8px 0px 8px;height: inherit;border:0px;">
		<el-tab-pane
		 	:key="item.name"
			v-for="(item, index) in editableTabs"
			:label="item.title"
			:name="item.name"
			style="width: 100%;overflow:auto;height:100%"
		>
			<span slot="label"><i :class="item.iconClass"></i> {{item.title}}</span>
			<div :is="item.content"></div>
		</el-tab-pane>
	</el-tabs>
</template>
<script>
export default {
  data() {
    return {
      editableTabsValue: "0",
      editableTabs: [],
      tabIndex: 0
    };
  },
  watch: {
    $route(to, from) {
      this.addTab(
        this.$route.params.path,
        this.$route.params.subPath,
        this.$route.params.page
      );
    }
  },
  mounted: function() {
    this.addTab(
      this.$route.params.path,
      this.$route.params.subPath,
      this.$route.params.page
    );
    /*if(!this.$route.params.page)
			window.localStorage.setItem('nowurl', 'ww')*/
    //如果路径不为空，定位到相应侧边栏
  },
  methods: {
    addTab(path, subPath, page) {
      var flag = false;
      var tabs = this.editableTabs;
      var targetName = path + "-" + subPath + "-" + page;
      var obj = tabs.find(function(value, index, arr) {
        return value["name"] == targetName;
      });
      //console.log(obj);
      if (typeof obj != "undefined") {
        this.editableTabsValue = targetName;
      } else {
        try {
          this.editableTabs.push({
            title: chg[page],
            name: targetName,
            iconClass: "el-icon-message",
            content: require("../../" +
              path +
              "/" +
              subPath +
              "/" +
              page +
              ".vue")
          });
          this.editableTabsValue = targetName;
        } catch (err) {
          console.log("路徑錯誤");
        }
      }
    },
    removeone(targetName) {
      let tabs = this.editableTabs;
      let activeName = this.editableTabsValue;
      if (activeName === targetName) {
        tabs.forEach((tab, index) => {
          if (tab.name === targetName) {
            let nextTab = tabs[index + 1] || tabs[index - 1];
            if (nextTab) {
              activeName = nextTab.name;
            }
          }
        });
      }
      this.editableTabsValue = activeName;
      this.editableTabs = tabs.filter(tab => tab.name !== targetName);
    },
    locationsider(tab) {
      var index = "/" + tab.name.split("-").join("/");
      //console.log(this.$store.state.nowurl);
      //this.$store.state.nowurl=index;
      this.$router.push(index);
      //window.localStorage.setItem('nowurl', index);
    }
  }
};
</script>