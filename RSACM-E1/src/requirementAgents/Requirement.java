package requirementAgents;

import behaviours.require.RequireCheckStatus;
import behaviours.require.RequireEvent;
import jade.core.AID;
import jade.core.Agent;
import jade.core.behaviours.TickerBehaviour;
import util.JadeUtil;
import util.RequirementList;

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
    public static Map<String, Long> retrieveTime = new HashMap<>();
    public static Map<String, Long> propagationTime = new HashMap<>();

    @Override
    protected void setup() {
        System.out.println("需求agent已加载,noiseRate="+noiseRate);
        requirementsList = (Map<String, List<RequirementList>>) getArguments()[0];
        updatedFunctions = (Map<String, Integer>) getArguments()[1];
        requireEnd = requirementsList.size() + 1;
//        requireEnd = 241;
        addBehaviour(new TickerBehaviour(this, JadeUtil.getTimePeriod()) {
            @Override
            protected void onTick() {
                updatedFunctions.clear();
                if (period >= requireEnd) {
                    System.out.println("请求数：" + requireNum + ",成功数：" + succeedNum.get());
                    System.out.println("--------------------实验结束--------------------");
                    myAgent.doWait(1000);
                    System.exit(0);
//                    myAgent.doDelete();

                } else {
                    System.out.println(
                            "------------------------" + JadeUtil.getDateTime() + ":正在开始第" + period + "周期" +
                                    "------------------------");
                    System.out.println("请求数：" + requireNum + ",成功数：" + succeedNum.get());
//                    ArrayList<RequirementBean2> requirementList = (ArrayList<RequirementBean2>) requirementsList.get(
//                            requireStart + "周期");
                    requireStart++;
                    AtomicInteger stepChain = new AtomicInteger(-1);
                    myAgent.addBehaviour(new RequireEvent(stepChain, noiseRate,period));
                    myAgent.addBehaviour(new RequireCheckStatus(stepChain, root, period, updatedFunctions,noiseRate));
                    period++;

                }

            }
        });
    }

}
