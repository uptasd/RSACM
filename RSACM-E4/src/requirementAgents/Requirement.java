package requirementAgents;

import behaviours.require.RequireCheckStatus;
import behaviours.require.RequireEvent;
import behaviours.require.RequireService;
import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.TickerBehaviour;
import util.RequirementInfo;
import util.RequirementList;
import util.JadeUtil;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

public class Requirement extends Agent {
    private int requireNum = 0;

    private int period = 1;

    int noiseRate = 40;
    Map<String, List<RequirementList>> requirementsList;
    AID root = new AID("中山大学第三附属医院-医院功能", AID.ISLOCALNAME);
    int requireStart = 1;
    int requireEnd = 0;
    AtomicInteger succeedNum = new AtomicInteger(0);
    public static Map<String, Integer> updatedFunctions = null;
    public static Map<String, Integer> affectedAgent = new HashMap<>();
    public static Map<String, Integer> affectedRes = new HashMap<>();
    public static Map<String, Long> retrieveTime = new HashMap<>();
    public static Map<String, Long> propagationTime = new HashMap<>();
    public static Map<String, String> hitRate = new HashMap<>();

    @Override
    protected void setup() {
        System.out.println("需求agent已加载，噪声率为:" + noiseRate);
        requirementsList = (Map<String, List<RequirementList>>) getArguments()[0];
        updatedFunctions = (Map<String, Integer>) getArguments()[1];
        requireEnd = requirementsList.size() + 1;

//        requireEnd = 241;
        addBehaviour(new RequireCheckStatus(new AtomicInteger(0), root, 0,
                                            updatedFunctions, noiseRate, true));

        addBehaviour(new TickerBehaviour(this, JadeUtil.getTimePeriod()) {
            @Override
            protected void onTick() {
                updatedFunctions.clear();
                if (period >= requireEnd) {
                    System.out.println("请求数：" + requireNum + ",成功数：" + succeedNum.get());
                    System.out.println("--------------------实验结束--------------------");
                    myAgent.doWait(1000);
                    System.exit(0);

                } else {
                    System.out.println(
                            "------------------------" + JadeUtil.getDateTime() + ":正在开始第" + period + "周期" +
                                    "------------------------");
                    System.out.println("请求数：" + requireNum + ",成功数：" + succeedNum.get());
                    ArrayList<RequirementList> requirementList = (ArrayList<RequirementList>) requirementsList.get(
                            requireStart + "周期");
                    requireStart++;
                    AtomicInteger stepChain = new AtomicInteger(-1);
                    myAgent.addBehaviour(new RequireEvent(stepChain, noiseRate, period, affectedRes));
                    myAgent.addBehaviour(new RequireCheckStatus(stepChain, root, period, updatedFunctions, noiseRate));
                    requireNum += requirementList.size();
                    int r_index = 0;
                    int processCnt = 0;
                    int processNum = 0;
                    for (RequirementList requirements : requirementList) {
                        ArrayList<String> rq = (ArrayList<String>) requirements.getRequirements();
                        processNum += rq.size();
                    }
                    for (RequirementList requirements : requirementList) {
                        r_index++;
                        ArrayList<String> rq = (ArrayList<String>) requirements.getRequirements();
                        String qos = requirements.getQos();
                        Integer urgencyLevel = requirements.getUrgencyLevel();
                        AtomicInteger succeedPart = new AtomicInteger(0);
                        for (int i = 0; i < rq.size(); i++) {
                            String FunName = rq.get(i).split(":")[0];
                            Float requiredTime = Float.valueOf(rq.get(i).split(":")[1]);
                            AID requiredFun = new AID(FunName, AID.ISLOCALNAME);
                            RequirementInfo requirementInfo = new RequirementInfo();
                            requirementInfo.setRequiredFunction(requiredFun);
                            requirementInfo.setRequiredTime(requiredTime);
                            requirementInfo.setUrgencyLevel(urgencyLevel);
                            requirementInfo.setRequireQos(qos);
                            String nextRequirement = "None";
                            if (i <= rq.size() - 2) {
                                nextRequirement = rq.get(i + 1).split(":")[0];
                            }
                            processCnt++;
                            myAgent.addBehaviour(
                                    new RequireService(r_index, stepChain, i + 1, processCnt, period, requirementInfo,
                                                       nextRequirement,
                                                       succeedPart,
                                                       succeedNum,
                                                       rq.size(), processNum, updatedFunctions, affectedAgent,
                                                       retrieveTime, propagationTime, hitRate,
                                                       noiseRate));
                        }
                    }
                    period++;

                }

            }
        });
    }

}
