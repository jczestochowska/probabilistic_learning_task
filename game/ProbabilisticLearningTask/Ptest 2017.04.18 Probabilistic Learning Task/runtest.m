function runtest(filename, CycleNo, MinimumBlocks, MaximumBlocks)

    clear Stimulus;
    global Stimulus;

   
    %****************
    TrainingCycleLength = 3;
    %****************

    
    if exist('stimuli.mat','file')
        
        load stimuli.mat;
        
    else
        
        listing = dir('hira');
        listing(1:2) = [];
        Nhira = length(listing);
        indices = randperm(Nhira);
        indices = indices(1:6);
        Stimulus{1} = imread(strcat('hira\',listing(indices(1)).name),'BackgroundColor',[1 1 1]);
        Stimulus{2} = imread(strcat('hira\',listing(indices(2)).name),'BackgroundColor',[1 1 1]);
        Stimulus{3} = imread(strcat('hira\',listing(indices(3)).name),'BackgroundColor',[1 1 1]);
        Stimulus{4} = imread(strcat('hira\',listing(indices(4)).name),'BackgroundColor',[1 1 1]);
        Stimulus{5} = imread(strcat('hira\',listing(indices(5)).name),'BackgroundColor',[1 1 1]);
        Stimulus{6} = imread(strcat('hira\',listing(indices(6)).name),'BackgroundColor',[1 1 1]);
        listing = dir('hiratest');
        listing(1:2) = [];
        Stimulus{7} = imread(strcat('hiratest\',listing(1).name),'BackgroundColor',[1 1 1]);
        Stimulus{8} = imread(strcat('hiratest\',listing(2).name),'BackgroundColor',[1 1 1]);
        Stimulipermutation = randperm(length(Stimulus)); % permute the sequence of stimuli read out from png files
        Stimulus = Stimulus(Stimulipermutation);
        % succesive pairs are {1,2} {3,4} {5,6}
        ProbRew = [80 20 70 30 60 40]/100;  % save to stimuli.mat file

        save('stimuli.mat', 'Stimulus', 'ProbRew', 'Stimulipermutation');

    end
    
    h = InitScreen();
    %##############################
    testOK = 0;
    while testOK == 0
        Showtext(['ProszÍ przeczytaÊ uwaønie poniøszπ instrukcjÍ.' char(10) char(10) ...
            'Na ekranie bÍdπ prezentowane pary rÛønych symboli.' char(10) char(10) ...
            'Jeden z nich jest "szczÍúliwy" a drugi "pechowy".' char(10) ...
            'Na poczπtku nie bÍdziesz wiedzieÊ, ktÛry jest ktÛry.' char(10) char(10) ...
            'WybÛr "szczÍúliwego" symbolu daje wiÍkszπ szansÍ na nagrodÍ (napis "\color{blue}Dobrze\color{black}").' char(10) ...
            'Czasem powoduje jednak pojawienie siÍ kary (napis "\color{red}èle\color{black}").' char(10) char(10) ...
            'Twoim celem jest zebranie jak najwiÍkszej liczby nagrÛd.' char(10) char(10) ...
            'Naciúnij spacjÍ by kontynuowaÊ.'], 25, 'black'); 
        waitforbuttonpress
        Showtext(['SzczÍúliwy symbol proszÍ wskazywaÊ uøywajπc nastÍpujπcych klawiszy:' char(10) char(10) ...
            '"1" - wybÛr symbolu po lewej stronie,' char(10) char(10) ...
            '"0" - wybÛr symbolu po prawej stronie.' char(10) char(10) ...
            'Wyboru naleøy dokonywaÊ jak najszybciej (w ciπgu 3 sekund).' char(10) char(10) ...
            'Naciúnij spacjÍ by kontynuowaÊ.'], 25, 'black')
        waitforbuttonpress
        Showtext(['Zbierz jak najwiÍcej nagrÛd samodzielnie oceniajπc kolejne prezentowane symbole.' char(10) char(10) ...
            'Naciúnij spacjÍ by kontynuowaÊ.'], 25, 'black')
        waitforbuttonpress
        Showtext(['Zanim zaczniemy badanie' char(10) ...
            'sprawdzimy czy w≥aúciwie rozumiesz podane instrukcje.' char(10) char(10) ...
            'ProszÍ odpowiedzieÊ na kilka pytaÒ dotyczπcych instrukcji.' char(10) char(10) ...
            'Naciúnij spacjÍ by kontynuowaÊ.'], 25, 'black')
        waitforbuttonpress
        Showtext(['Jakim klawiszem wybiera siÍ symbol z lewej strony?' char(10) char(10) ...
            'Udziel odpowiedzi, wciskajπc odpowiedni klawisz ...'], 25, 'black');
        ans2 = getkeywaitD(100,'full');
        Showtext(['Jakim klawiszem wybiera siÍ symbol z prawej strony?' char(10) char(10) ...
            'Udziel odpowiedzi, wciskajπc odpowiedni klawisz ...'], 25, 'black');
        ans3 = getkeywaitD(100,'full');
        if ans2 == '1' && ans3 == '0'
            testOK = 1;
        else
            Showtext(['Co najmniej jedna z odpowiedzi jest nieprawid≥owa.' char(10) char(10) ...
            'Instrukcja zostanie powtÛrzona.' char(10) char(10) ...
            'Naciúnij spacjÍ by kontynuowaÊ.'], 25, 'black');
        waitforbuttonpress
        end
    end
    %##############################
    Showtext(['åwietnie! Niebawem przejdziemy do w≥aúciwego badania.' char(10) char(10) ...
        'Przed prezentacjπ kaødej pary symboli zobaczysz planszÍ z zielonym kÛ≥kiem.' char(10) char(10) ...
        'Po≥Ûø rÍce na klawiaturze w taki sposÛb aby da≥o siÍ swobodnie naciskaÊ klawisze "1" i "0".' char(10) char(10) ...
        'Naciúnij spacjÍ by kontynuowaÊ.'], 25, 'black');
    waitforbuttonpress
    Showtext(['Na poczπtek kilka par symboli na prÛbÍ.' char(10) char(10) ...
        'Naciúnij spacjÍ by kontynuowaÊ.'], 25, 'black');   
    waitforbuttonpress
    
    for i = 1:6
        Showfocuspoint(0.2,0.5);
        ShowTrial(7,8,[1 0]','Feedback');
    end
    
    Showtext(['åwietnie!' char (10) char(10) ...
        'Naciúnij spacjÍ by kontynuowaÊ.'], 25, 'black');
    waitforbuttonpress
    Showtext(['Teraz rozpocznie siÍ w≥aúciwa czÍúÊ badania.' char(10) char(10) ...
        'Tak jak do tej pory:' char(10) char(10) ...
        '"1" - wybÛr symbolu po lewej stronie,' char(10) char(10) ...
        '"0" - wybÛr symbolu po prawej stronie.' char(10) char(10) ...
        'Naciúnij spacjÍ by kontynuowaÊ.'], 25, 'black');
    waitforbuttonpress
    Showtext('Przygotuj siÍ!', 25, 'black');
    pause(2)    
    
    %############################  Normal Trials ##############################
    StimulusHistory = [];
    StimulusHistoryLeft = [];
    StimulusHistoryRight = [];
    ActionHistory = [];
    CorrectActionHistory = [];
    RewardHistory = [];
    RTimeHistory = [];
    
    
    moreBlocks = 1; % if subject did not learn contingencies, then the next block goes on
    b = 1;
    while moreBlocks == 1 && b <= MaximumBlocks
    
        % ^^^^^^^^^ training cycle ^^^^^^^^^
        ABcorrect(b) = 0;
        CDcorrect(b) = 0;
        EFcorrect(b) = 0;

        ActionBlockHistory = zeros(1,TrainingCycleLength*CycleNo);
        CorrectActionBlockHistory = zeros(1,TrainingCycleLength*CycleNo);
        RewardBlockHistory = zeros(1,TrainingCycleLength*CycleNo);
        RTimeBlockHistory = zeros(1,TrainingCycleLength*CycleNo);
        StimulusBlockHistory = zeros(1,TrainingCycleLength*CycleNo);
        StimulusBlockHistoryLeft = zeros(1,TrainingCycleLength*CycleNo);
        StimulusBlockHistoryRight = zeros(1,TrainingCycleLength*CycleNo);        
        
        for c = 1:CycleNo
            
            pairs = 1:TrainingCycleLength; % numbers of all training pairs
            pairs = pairs(randperm(TrainingCycleLength));
            if c > 1
                while pairs(1) == StimulusBlockHistory(TrainingCycleLength*(c-1))
                    pairs = pairs(randperm(TrainingCycleLength));
                end
            else
                if b > 1
                    while pairs(1) == StimulusHistory(length(StimulusHistory))
                        pairs = pairs(randperm(TrainingCycleLength));
                    end
                end
            end
            StimulusBlockHistory(TrainingCycleLength*(c-1)+1:TrainingCycleLength*c) = pairs;
            
        end
        
        RewardsGrantedA = zeros(1,CycleNo);
        RewardsGrantedB = zeros(1,CycleNo);
        RewardsGrantedC = zeros(1,CycleNo);
        RewardsGrantedD = zeros(1,CycleNo);
        RewardsGrantedE = zeros(1,CycleNo);
        RewardsGrantedF = zeros(1,CycleNo);        
        RewardsGrantedA(1:floor(CycleNo*ProbRew(1))) = 1;
        RewardsGrantedB(1:floor(CycleNo*ProbRew(2))) = 1;
        RewardsGrantedC(1:floor(CycleNo*ProbRew(3))) = 1;
        RewardsGrantedD(1:floor(CycleNo*ProbRew(4))) = 1;   
        RewardsGrantedE(1:floor(CycleNo*ProbRew(5))) = 1;
        RewardsGrantedF(1:floor(CycleNo*ProbRew(6))) = 1;    
        RewardsGranted = zeros(2,TrainingCycleLength*CycleNo);
        
        idx1 = StimulusBlockHistory == 1;
        idx2 = StimulusBlockHistory == 2;
        idx3 = StimulusBlockHistory == 3;
        RewardsGranted(1,idx1) = RewardsGrantedA(randperm(CycleNo));
        RewardsGranted(2,idx1) = RewardsGrantedB(randperm(CycleNo));
        RewardsGranted(1,idx2) = RewardsGrantedC(randperm(CycleNo));
        RewardsGranted(2,idx2) = RewardsGrantedD(randperm(CycleNo));
        RewardsGranted(1,idx3) = RewardsGrantedE(randperm(CycleNo));
        RewardsGranted(2,idx3) = RewardsGrantedF(randperm(CycleNo));
        
        for i = 1:TrainingCycleLength*CycleNo          
            
            Showfocuspoint(0.2,0.5);
            [ActionBlockHistory(i), RewardBlockHistory(i), RTimeBlockHistory(i), ...
                StimulusBlockHistoryLeft(i), StimulusBlockHistoryRight(i), CorrectActionBlockHistory(i)] ...
                = ShowTrial(2*StimulusBlockHistory(i)-1, 2*StimulusBlockHistory(i), RewardsGranted(:,i), 'Feedback');
            
        end
        
        ABcorrect(b) = sum((CorrectActionBlockHistory == 1) .* (StimulusBlockHistory == 1));
        CDcorrect(b) = sum((CorrectActionBlockHistory == 1) .* (StimulusBlockHistory == 2));
        EFcorrect(b) = sum((CorrectActionBlockHistory == 1) .* (StimulusBlockHistory == 3));
            
        StimulusHistory = [StimulusHistory StimulusBlockHistory];
        StimulusHistoryLeft = [StimulusHistoryLeft StimulusBlockHistoryLeft];
        StimulusHistoryRight = [StimulusHistoryRight StimulusBlockHistoryRight];
        ActionHistory = [ActionHistory ActionBlockHistory];
        CorrectActionHistory = [CorrectActionHistory CorrectActionBlockHistory];
        RewardHistory = [RewardHistory RewardBlockHistory];
        RTimeHistory = [RTimeHistory RTimeBlockHistory];       
        
        ABperformance(b) = ABcorrect(b) / CycleNo;
        CDperformance(b) = CDcorrect(b) / CycleNo;
        EFperformance(b) = EFcorrect(b) / CycleNo;
        
        mkdir(filename);
        save([filename '\' filename 'learning'], 'StimulusHistory', 'StimulusHistoryLeft', 'StimulusHistoryRight', 'ActionHistory', 'CorrectActionHistory', 'RewardHistory', 'RTimeHistory', ...
            'ABperformance','CDperformance','EFperformance');
        
        if b >= MinimumBlocks && ABperformance(b) >= 65/100 && CDperformance(b) >= 60/100 && EFperformance(b) >= 50/100
            moreBlocks = 0;
        end
        
        b = b + 1;
        if moreBlocks == 1 && b <= MaximumBlocks && b >= MinimumBlocks
            Showtext(['Spora czÍúÊ badania zosta≥a wykonana.' char(10) char(10) ...
                'Jeøeli potrzebujesz, moøesz zrobiÊ sobie chwilÍ przerwy.' char(10) char(10) ...
                'Naciúnij spacjÍ by kontynuowaÊ.'], 25, 'black');
            waitforbuttonpress           
        end
        
    end
    % ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    %####################################################################
    Showtext(['DziÍkujemy za wykonanie pierwszej czÍúci badania.' char(10) char(10)...
        'W tej chwili zapisywany jest raport z jej przebiegu...'], 25, 'black');
    pause(1)
    save([filename '\' filename 'learning'], 'StimulusHistory', 'StimulusHistoryLeft', 'StimulusHistoryRight', 'ActionHistory', 'CorrectActionHistory', 'RewardHistory', 'RTimeHistory');
    SaveToExcel([filename '\' filename 'learning'], 1, {'A1', 'B1', 'A2', 'B2', 'A3', 'B3', 'A4', 'B4', 'A5', 'B5', 'A6', 'B6', 'A7', 'B7'}, {{'StimulusPair'}, StimulusHistory, {'StimulusLeft'}, StimulusHistoryLeft, {'StimulusRight'}, StimulusHistoryRight, ...
        {'Action'}, ActionHistory, {'Was the Action Correct?'}, CorrectActionHistory, {'Reward'}, RewardHistory, {'Response time'}, RTimeHistory});
    Showtext(['ZakoÒczono zapisywanie raportu do pierwszej czÍúci badania.' char(10) char(10) ...
        'Naciúnij spacjÍ by zakoÒczyÊ.'], 25, 'black');
    waitforbuttonpress
    quit
%     Showtext(['W tej czÍúci badania po Twoich wyborach nie bÍdπ siÍ pojawia≥y nagrody ani kary.' char(10) ...
%          'Wybieraj te symbole, ktÛre dotychczas by≥y bardziej "szczÍúliwe".' char (10) char(10) ...
%          'Naciúnij spacjÍ by kontynuowaÊ.'], 25, 'black');
%     waitforbuttonpress
%     Showtext(['Wszystkie symbole pojawia≥y siÍ w poprzedniej czÍúci badania,' char(10) ...
%          'ale tym razem mogπ byÊ zestawione w parach, ktÛrych wczeúniej nie by≥o.' char(10) char(10) ...
%          'Wybierz wÛwczas ten symbol, ktÛry wydaje Ci siÍ lepszy.' char (10) char(10) ...
%          'Jeúli nie masz pewnoúci, ktÛry symbol wybraÊ, zaufaj swojej intuicji.' char(10) char(10) ...
%          'Naciúnij spacjÍ by kontynuowaÊ.'], 25, 'black');
%     waitforbuttonpress    
%     Showtext('Przygotuj siÍ!', 25, 'black');
%     pause(3)    
%     % generate all possible pairs
%     M = 6;
%     TotalPairs = M*(M-1)/2;
%     stimulipairs = zeros(TotalPairs,3);
%     k = 1;
%     for i = 1:M-1
%         for j = i+1:M
%             stimulipairs(k,1:2) = [i j];
%             k = k + 1;
%         end
%     end
%     % assign weights to pairs (1 to previeously learned pairs, 6 to new
%     % pairs)
%     occurence = zeros(1,length(stimulipairs));
%     for i = 1:length(stimulipairs)
%         if stimulipairs(i,1) == 1 && stimulipairs(i,2) == 2 ...
%             || stimulipairs(i,1) == 3 && stimulipairs(i,2) == 4 ...
%             || stimulipairs(i,1) == 5 && stimulipairs(i,2) == 6
%             occurence(i) = 1;
%         else
%             occurence(i) = 6;
%         end
%     end
%     for i = 1:length(stimulipairs)
%         stimulipairs(i,:) = [stimulipairs(i,1:2) occurence(i)];
%     end
%     
%     stimulipairs = sortrows(stimulipairs,3);
%     oldstimulipairs = stimulipairs(stimulipairs(:,3) == 1,:);
%     newstimulipairs = stimulipairs(stimulipairs(:,3) == 6,:);
%     oldstimulipairs(:,3) = [];
%     newstimulipairs(:,3) = [];
%     
%     stimulisession = [oldstimulipairs; newstimulipairs(randperm(length(newstimulipairs)),:)];
%     for i = 2:6
%         
%         addstimulipairs = newstimulipairs(randperm(length(newstimulipairs)),:);
%         while addstimulipairs(1,1) == stimulisession(length(stimulisession),1) && addstimulipairs(1,2) == stimulisession(length(stimulisession),2)
%             addstimulipairs = newstimulipairs(randperm(length(newstimulipairs)),:);
%         end
%         stimulisession = [stimulisession; addstimulipairs];
%         
%     end
% 
%     StimulusHistoryLeft = stimulisession(:,1)';
%     StimulusHistoryRight = stimulisession(:,2)';
%     ActionHistory = zeros(1,length(stimulisession));
%     RTimeHistory = zeros(1,length(stimulisession));
%     
%     for i = 1 : length(stimulisession)
%                 
%         Showfocuspoint(0.2,0.5);
%         [ActionHistory(i), ~, RTimeHistory(i), ~, ~, ~] = ShowTrial(stimulisession(i,1),stimulisession(i,2), [], 'No Feedback');
%         save([filename '\' filename 'testing'], 'StimulusHistoryLeft', 'StimulusHistoryRight', 'ActionHistory', 'RTimeHistory');    
%         
%     end
%     %####################################################################
%     
%     Showtext(['DziÍkujemy za dotychczasowy wysi≥ek. Juø prawie jesteúmy przy koÒcu badania.' char(10) char(10) ...
%             'Zosta≥o tylko ostatnie krÛtkie zadanie.' char(10) char(10) ... 
%             'Na nastÍpnych planszach pojawiπ siÍ kolejno wszystkie symbole.' char(10) ...
%             'Przy kaødym z nich, wyobraü sobie, øe wybierasz go 100 razy pod rzπd.' char(10) ...
%             'Jak czujesz, ile wÛwczas nagrÛd (mniej wiÍcej) moøna za niego otrzymaÊ?' char(10) char(10) ...
%             'Pod symbolem bÍdzie suwak, ktÛry moøesz ustawiÊ w pozycji od 0 - zawsze pechowy' char(10) ...
%             'aø do 100 - zawsze szczÍúliwy. Moøesz uøyÊ kursora do przesuwania suwakiem,' char(10) ...
%             'lub strza≥ek po obu stronach suwaka.' char(10) ...
%             'Potwierdzasz, klikajπc kursorem w przycisk OK.' char(10) char(10) ... 
%             'Naciúnij spacjÍ by kontynuowaÊ.'], 25, 'black');
%     waitforbuttonpress
%     
%     UserProbabilities = zeros(1,6);
%     for i = randperm(6)
%         cla
%         subplot(1,6,3);
%         q = subplot(1,6,3);
%         pos = get(q,'position'); % centering
%         pos(1) = pos(1) + 0.05;
%         set(q, 'position', pos);
%         imshow(Stimulus{i});
%         slajder = uicontrol('Style', 'slider',...
%             'Min',0,'Max',100,'Value',50,...
%             'SliderStep', [0.05 0.05], ...
%             'Units','normalized', ...
%             'Position', [0.45 0.2 0.08 0.03],...
%             'BackgroundColor','white',...
%             'Callback', {@SetProb,h}); 
%         tekst = uicontrol('Style','text',...
%             'Units','normalized', ...
%             'Position',[0.471 0.27 0.04 0.05],...
%             'FontSize',27,...
%             'BackgroundColor','white',...
%             'String',50);
%         tekstP = uicontrol('Style','text',...
%             'Units','normalized', ...
%             'Position',[0.388 0.204 0.06 0.03],...
%             'FontSize',14,...
%             'BackgroundColor','white',...
%             'String','pechowy');
%         tekstS = uicontrol('Style','text',...
%             'Units','normalized', ...
%             'Position',[0.535 0.204 0.06 0.03],...
%             'FontSize',14,...
%             'BackgroundColor','white',...
%             'String','szczÍúliwy');
%         
%         ButtonOKHandle = uicontrol('Parent',h,'Style','pushbutton','String','OK','Position',[0.455 0.1 0.07 0.07],'Units','normalized', 'FontSize', 22);
%         set(ButtonOKHandle,'Callback',{@ButtonOKCallback, ButtonOKHandle});
%         waitfor(ButtonOKHandle);
%         UserProbabilities(i) = uint8(str2double(get(tekst,'String')));  
%         delete(slajder);
%         delete(tekst);
%         delete(tekstP);
%         delete(tekstS);
%     end    
%     Showtext(['Gratulacje! Ca≥e badanie zosta≥o ukoÒczone!' char(10) char(10) ...
%         'DziÍkujemy za jego wykonanie.' char(10) char(10) ...
%         'W tej chwili zapisywany jest raport koÒcowy...'], 25, 'black');
%     pause(1);
%     save([filename '\' filename 'testing'], 'StimulusHistoryLeft', 'StimulusHistoryRight', 'ActionHistory', 'RTimeHistory', 'UserProbabilities');
%     SaveToExcel([filename '\' filename 'testing'], 1, {'A1', 'B1', 'A2', 'B2', 'A3', 'B3', 'A4', 'B4'}, {{'StimulusLeft'}, StimulusHistoryLeft, ...
%        {'StimulusRight'}, StimulusHistoryRight, {'Action'}, ActionHistory, {'Response time'}, RTimeHistory});
%     SaveToExcel([filename '\' filename 'testing'], 2, {'A1', 'B1', 'A2', 'B2'}, {{'StimulusNo'}, 1:6, {'UserProbabilities'}, UserProbabilities});
%     Showtext(['ZakoÒczono zapisywanie raportu.' char(10) char(10) ...
%               ' DziÍkujemy.'], 25, 'black');
%     pause(2);
    
    
    function SetProb(hObj,event,ax) 
        val = get(hObj,'Value');
        remainder_5 = mod(val,5);
        if remainder_5 < 2.5
           val = floor(val - remainder_5);
        else
           val = ceil(val - remainder_5 + 5);
        end
        set(tekst,'String',num2str(val));
    end
 

end % function runtest

function ButtonOKCallback(hObject,event, ButtonOKHandle)

    delete(ButtonOKHandle);
    
end

function [ Action, Reward, RTime, LStimulusNo, RStimulusNo, CorrectAction] = ShowTrial( LeftStimulusNo, RightStimulusNo, RewardsGranted, tmode)
    
    global Stimulus;
    
    %****************
    MaxResponseTime = 3;
    FeedbackPresentationTime = 0.5;
    %****************
    
    posLeft = -0.025 - 0.02;
    posRight = 0.0   + 0.02;
    
    % clear screen
    for i = 1:6
        subplot(1,6,i);
        axis off;
        cla
    end
    
    if randi(2) == 1
        LStimulusNo = LeftStimulusNo;
        RStimulusNo = RightStimulusNo;
        if strcmp(tmode,'Feedback') == 1
            LRewardGranted = RewardsGranted(1);
            RRewardGranted = RewardsGranted(2);
            BetterStimulus = '1';
        end
    else
        LStimulusNo = RightStimulusNo;
        RStimulusNo = LeftStimulusNo;
        if strcmp(tmode,'Feedback') == 1
            LRewardGranted = RewardsGranted(2);
            RRewardGranted = RewardsGranted(1);     
            BetterStimulus = '0';
        end
    end
    cla
    % left stimulus
    q = subplot(1,6,3);
    pos = get(q,'position');
    pos(1) = pos(1) + posLeft;
    set(q, 'position', pos);
    imshow(Stimulus{LStimulusNo});
    
    %right stimulus
    q = subplot(1,6,4);
    pos = get(q,'position');
    pos(1) = pos(1) + posRight;
    set(q, 'position', pos);
    imshow(Stimulus{RStimulusNo});
    
    % read the choice
    tic;
    Action = getkeywaitD(MaxResponseTime,'leftright');
    RTime = toc;
    if strcmp(tmode,'Feedback') == 1
        if strcmp(Action, BetterStimulus) == 1
            CorrectAction = 1;
        else
            CorrectAction = 0;
        end
    else
        CorrectAction = [];
    end

    % clear screen before showing feedback
    for i = 1:6
        subplot(1,6,i);
        axis off;
        cla
    end
    q = subplot(1,7,4);
    pos = get(q,'position');
    pos(1) = pos(1) - 0.015;
    set(q, 'position', pos);
    
    switch Action 
        case '1'   % left stimulus chosen
            Action = 1;
            if strcmp(tmode,'Feedback') == 1
                Reward = LRewardGranted;
                if Reward == 0
                    Reward = -1;
                    Showtext('èle', 50, 'red');          
                else
                    Showtext('Dobrze', 50, 'blue');  
                end
            end
        
        case '0'   % right stimulus chosen
            Action = 0;
            if strcmp(tmode,'Feedback') == 1
                Reward = RRewardGranted;
                if Reward == 0
                    Reward = -1;
                    Showtext('èle', 50, 'red');
                else
                    Showtext('Dobrze', 50, 'blue');
                end
            end
            
        otherwise
            Action = -1;
            Reward = 0;
            RTime = -1;
            Showtext('Nie udzieli≥eú øadnej odpowiedzi', 25, 'red');
        
    end
    
    if strcmp(tmode,'Feedback') == 1
        pause(FeedbackPresentationTime);
    else
        Reward = [];
        if Action == -1
            pause(FeedbackPresentationTime);
        end
    end

end

function h = InitScreen()

    h = figure('Color','white', 'Menu','none');
    jFrame = get(handle(gcf),'JavaFrame');
    pause(0.01);
    jFrame.setMaximized(true);

end


function Showtext( message, fsize, color )

    subplot(1,1,1);
    cla;
    text(0.5, 0.5, message, 'Rotation', 0, 'FontSize', fsize, 'Color',color, ...
        'HorizontalAlignment','Center', 'VerticalAlignment','Middle')
    axis off;
    
end


function Showfocuspoint(MinTime, MaxTime)
    
    subplot(1,1,1);
    cla;
    rectangle('Position',[-10,-3.65,5,5],'Curvature',[1,1],'EdgeColor','white','FaceColor',[0 0.7 0]); axis equal; axis([-100 100 -100 100]);
    set(gca,'xcolor','w','ycolor','w','xtick',[],'ytick',[])
    set(gcf,'KeyPressFcn',@keypress_callback);
    pause((MaxTime-MinTime)*rand + MinTime);
    
end


 function SaveToExcel(filename, sheet, xlRange, Text)
 
     n = length(xlRange);
     for i = 1:n
         xlswrite(filename,Text{i},sheet,xlRange{i});
     end
     
 end


function keypress_callback(gcbo,event)

    switch event.Key
    end
    
end


function ch = getkeywaitD(m, kmode) 

    figh = figure('windowstyle','modal','position',[-100 -100 1 1],'KeyPressFcn',@(obj,evt) 0);
    waitfor(gcf,'CurrentCharacter');
    t0 = clock;
    curkey = '';
    switch kmode
        case 'full'
            curkey = get(gcf,'CurrentCharacter');
        case 'yesno'
            while etime(clock,t0) < m && strcmp(curkey,'t') == 0 && strcmp(curkey,'n') == 0
                curkey = get(gcf,'CurrentCharacter');
                pause(.05);
            end
            
        otherwise
            while etime(clock,t0) < m && strcmp(curkey,'1') == 0 && strcmp(curkey,'0') == 0
                curkey = get(gcf,'CurrentCharacter');
                pause(.05);
            end
    end
    
    if isempty(curkey)
        curkey = '-1';
    end
    delete(figh);
    ch = curkey;
    
end








