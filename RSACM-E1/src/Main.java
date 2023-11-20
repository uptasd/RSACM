import resourceAgents.ResourceBean;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import jade.core.Profile;
import jade.core.ProfileImpl;
import jade.core.Runtime;
import jade.wrapper.AgentController;
import jade.wrapper.ContainerController;
import jade.wrapper.StaleProxyException;
import util.JadeUtil;
import util.RequirementList;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class Main {
    static Map<String, Set<String>> replaceView = new ConcurrentHashMap<>();
    static Map<String, Integer> updatedFunctions = new ConcurrentHashMap<>();
    public static boolean deleteDir(String path) {
        File file = new File(path);
        if (!file.exists()) {//判断是否待删除目录是否存在
            System.err.println("The dir are not exists!");
            return false;
        }
        String[] content = file.list();//取得当前目录下所有文件和文件夹
        for (String name : content) {
            File temp = new File(path, name);
            if (temp.isDirectory()) {//判断是否是目录
                deleteDir(temp.getAbsolutePath());//递归调用，删除目录里的内容
                temp.delete();//删除空目录
            } else {
                if (!temp.delete()) {//直接删除文件
                    System.err.println("Failed to delete " + name);
                }
            }
        }
        return true;
    }

    public static void main(String[] args) throws IOException, StaleProxyException {
        String output_path = JadeUtil.outputPath;
        deleteDir(output_path);
        Runtime rt = Runtime.instance();
        Profile p = new ProfileImpl();
        p.setParameter("jade_domain_df_maxresult", "2110");
        p.setParameter(Profile.MAIN_HOST, "localhost");
        p.setParameter(Profile.GUI, "false");
        ContainerController cc = rt.createMainContainer(p);
        AgentController ac;
        ObjectMapper mapper = new ObjectMapper();
        String asset_dir = "asset/asset-small/";
        File file = new File(asset_dir + "function_agents.json");
        File file2 = new File(asset_dir + "resource_agents.json");
//        File file3 = new File(asset_dir + "requirementsSingle.json");
        File file3 = new File(asset_dir + "requirementsMulti.json");
        File file4 = new File(asset_dir + "replaceMapDemo.json");
        Map<String, List<RequirementList>> requirementsList = mapper.readValue(file3,
                                                                               new TypeReference<Map<String, List<RequirementList>>>() {
                                                                                });
        Map<String, ArrayList<String>> replacementMap = mapper.readValue(file4, new TypeReference<>() {
        });


        Map<String, Map<String, List>> mp = mapper.readValue(file, new TypeReference<>() {
        });
        Map<String, ResourceBean> res = mapper.readValue(file2,
                                                         new TypeReference<Map<String, ResourceBean>>() {
                                                         });
        for (Map.Entry entry : mp.entrySet()) {
            Map<String, List> neighbors = (Map<String, List>) entry.getValue();
            Object[] ob = new Object[]{neighbors, replacementMap, replaceView,updatedFunctions};
            String funName = (String) entry.getKey();

            ac = cc.createNewAgent(funName, "functionAgents.FunctionAgent", ob);
            ac.start();
        }
        for (Map.Entry entry : res.entrySet()) {
            ResourceBean a = (ResourceBean) entry.getValue();
            Object[] ob = new Object[]{a};
            ac = cc.createNewAgent((String) entry.getKey(), "resourceAgents.ResourceAgent", ob);
            ac.start();
        }

        Object[] requirements_arg = new Object[]{requirementsList,updatedFunctions};
        ac = cc.createNewAgent("Requirement", "requirementAgents.Requirement", requirements_arg);
        ac.start();
    }
}
