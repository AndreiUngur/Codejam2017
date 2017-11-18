def createScatter(range1, range2, n, y, x_label, y_label):
    x_min, x_max = range1.min() - 1, range1.max() + 1
    y_min, y_max = range2.min() - 1, range2.max() + 1
    plt.figure(n, figsize=(8, 6))
    plt.clf()
    
    # Plot the training points for Sepal
    plt.scatter(range1, range2, c=y, cmap=plt.cm.Set1,
            edgecolor='k')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())

def createPlot(x,y,x_label,y_label,n):
    plt.figure(n, figsize=(8, 6))
    plt.clf()
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)