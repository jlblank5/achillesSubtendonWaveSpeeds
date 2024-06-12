% radon transform function used to compute wave speeds

% INPUTS
% time = time vector (1 x n)
% u = nodal transverse displacements (m x n, where m is the number of
% nodes)
% z = proximal-distal location of nodes (1 x m)
% plotFigure = 0 (no plot) or 1 (plot)
% color = figure color (RGB, a vector)
function varargout = radonFunction(time,u,z,plotFigure,color)

    % sort nodal data wrt z
    [za,zidx] = sort(z(1,:));
    zpos = z(:,zidx);
    ydisp = u(:,zidx);

    % spatiotemporal plot
    amesh = []; zposmesh = [];
    for jj = 1:length(ydisp(1,:))
        z = zpos(1,jj);
        zposmesh = [zposmesh; z];
        amesh = [amesh ; ydisp(:,jj)'];
    end
    n = 1*length(zposmesh);
    zposmesh = interp1(1:length(zposmesh),zposmesh,linspace(1,length(zposmesh),n));
    amesh = interp1(1:size(amesh,1),amesh,linspace(1,size(amesh,1),n));
    [X,Y] = meshgrid(time,zposmesh);
    Z = amesh;

    % set up the filter
    arr=size(Z);
    filtt = true(arr);
    Height=arr(1);
    Width=arr(2);
    
    % brick wall filter to remove backwards reflections
    filtt(1:Height/2,1:Width/2) = 0;
    filtt(Height/2:end,Width/2:end) = 0;
    Yf = (fft2(Z));
    Yf_filt = filtt.*Yf;
    fft_filt = ifft2(Yf_filt);
    Z_filt = real(fft_filt);

    % Radon transform
    theta = -30:0.03:90;
    [R,xp] = radon(Z_filt,theta);
    maximum = max(max(R));
    [x,y]=find(R==maximum);
    idx_x=1*(mean(diff(zposmesh))); % z resolution
    idx_y=(1.*tand(theta(y)))*(mean(diff(time))); % computed time delay
    slope=idx_x/idx_y; % slope (SWS)
    varargout{1}=slope;
    arr=max(R); arr=arr-min(arr);

    % double Gaussian fit to determine average wave speed
    doubleGauss = @(c) c(3)*(1/(sqrt(2*pi)*c(1)))*exp(-0.5*((theta-c(2))/c(1)).^2) + c(4);
    errFun = @(c) sqrt(sum((arr-doubleGauss(c)).^2));
        
    % initial guesses, which can be modified
    initialGuess = [30 30 1 1];
    UB = [70 70 100 100];
    LB = [0 0 0 0];
    C = fminsearchbnd(errFun,initialGuess,LB,UB);
    Ytest=doubleGauss(C);
     
    % max index, corresponding to the shear wave speed
    [~,maxidx]=max(Ytest);
    locs=maxidx;

    % determine shear wave speed based upon index location
    if length(locs)> 1
         idx_x_min=1*(mean(diff(zposmesh))); % z resolution
         idx_y_min=(1.*tand(theta(locs(2))))*(mean(diff(time))); % computed time delay
         slopemin=idx_x_min/idx_y_min; % slope (SWS)
    
         idx_x_max=1*(mean(diff(zposmesh))); % z resolution
         idx_y_max=(1.*tand(theta(locs(1))))*(mean(diff(time))); % computed time delay
         slopemax=idx_x_max/idx_y_max; % slope (SWS)

         varargout{1}=[slopemin slopemax];
    else
         idx_x_max=1*(mean(diff(zposmesh))); % z resolution
         idx_y_max=(1.*tand(theta(locs(1))))*(mean(diff(time))); % computed time delay
         slopemax=idx_x_max/idx_y_max; % slope (SWS)

         varargout{1}=slopemax;
    end

    if plotFigure
        plot(theta,arr,'color',[color 0.5],'Linewidth',2); hold on
        Ytest = doubleGauss(C);
        hold on
        xlim([0 90])
        [~,maxidx]=max(Ytest);
        locs=maxidx;
        axis square
        xlabel('\theta [°]')
        ylabel('max \delta''')
    end
end
