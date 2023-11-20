package util;

import jade.core.AID;
import jade.core.Agent;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAException;

import java.text.SimpleDateFormat;
import java.util.Date;

public class JadeUtil {
    static long timePeriod = 5000;
    public static final String outputPath = "asset/output/";
    static SimpleDateFormat dateFormat = new SimpleDateFormat("HH:mm:ss.SSS");
    public static void register_service(Agent functionAgent, String serviceType, String serviceName) {
        DFAgentDescription dfd = new DFAgentDescription();
        dfd.setName(functionAgent.getAID());
        ServiceDescription sd = new ServiceDescription();
        ServiceDescription sd1 = new ServiceDescription();
        sd.setType(serviceType);
        sd.setName(serviceName);
        sd1.setType("Function");
        sd1.setName("Function");
        dfd.addServices(sd);
        dfd.addServices(sd1);
        try {
            DFService.register(functionAgent, dfd);
//            System.out.println("成功注册服务-" + sd.getName());
        } catch (FIPAException e) {
            e.printStackTrace();
            System.exit(-1);
        }
    }
    public static boolean search_agent_exist(Agent sourceAgent,String targetName) throws FIPAException {
        DFAgentDescription dfd = new DFAgentDescription();
        ServiceDescription sd = new ServiceDescription();
        sd.setName(targetName);
        dfd.addServices(sd);

        DFAgentDescription[] result = DFService.search(sourceAgent,dfd);
        if (result.length==0){
            return false;
        }else {
            return true;
        }
    }
//    public static int getRandomElement(int[] probability) {
//        //传入agg的概率数组，比如说第一个元素被选的概率是3/7，第二个是4/7，那么概率数组为[3,4]
//        int[] partialSum = new int[probability.length];
//        int sum = 0;
//        for (int i = 0; i < probability.length; i++) {
//            sum += probability[i];
//            partialSum[i] = sum;
//        }
//        int RandomNum = new Random().nextInt(sum)+1;
//        int pos=0;
//        for(int i=0;i<partialSum.length;i++){
//            if(RandomNum <= partialSum[i]){
//                pos=i;
//                break;
//            }
//        }
//        return pos;
//    }
    public static long getTimePeriod(){
        return timePeriod;
    }
    public static String getAgentName(AID agentIdentifier) {
        return agentIdentifier.getName().split("@")[0];
    }

    public static String getAgentName(Agent agent) {
        return agent.getAID().getName().split("@")[0];
    }
    public static String getAgentName(String agentName) {
        return agentName.split("@")[0];
    }

    public static String getDateTime() {
        return dateFormat.format(new Date());
    }
}
